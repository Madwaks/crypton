from abc import abstractmethod
from logging import Logger, getLogger
from typing import Iterator, List

from django.conf import settings
from django.core.cache import caches
from django.db import models
from django.db.models import ManyToManyRel
from django.urls import reverse

from utils.decorators import class_property

logger: Logger = getLogger("django")


class AbstractModel(models.Model):
    # Cache internals
    _cache_key_suffixes = tuple()

    class Meta:
        abstract = True

    def __str__(self):  # pragma: nocover
        return f"{self.pk}"

    @class_property
    def class_name_as_lowercase(cls) -> str:
        return cls.__name__.lower()

    @property
    def cache_keys(self):
        return (
            f"{self.cache_key}.{suffix}"
            for suffix in self.__class__._cache_key_suffixes
        )

    def save(self, *args, validation: bool = True, **kwargs):
        if validation:
            self.full_clean()
        self.clear_cache()
        super().save(*args, **kwargs)

    def clear_cache(self):
        cache = caches[settings.LRU_CACHE]
        cache.delete_many(self.cache_keys)

    def clear_specific_cache(self, key_suffix_list: List[str]):
        cache = caches[settings.LRU_CACHE]
        cache_keys = tuple(self.cache_keys)
        for key_suffix in key_suffix_list:
            key = f"{self.cache_key}.{key_suffix}"
            if key in cache_keys:
                cache.delete(key)

    @classmethod
    def add_cache_key(cls, key):
        if key not in cls._cache_key_suffixes:
            logger.debug(f"Adding '{key}' to {cls} key cache")
            cls._cache_key_suffixes = tuple([*cls._cache_key_suffixes, key])

    @classmethod
    def del_cache_key(cls, key):
        if key in cls._cache_key_suffixes:
            cls._cache_key_suffixes = tuple(
                [okey for okey in cls._cache_key_suffixes if okey != key]
            )

    @property
    def cache_key(self) -> str:
        return f"{self.class_name_as_lowercase}.{self.pk}"
