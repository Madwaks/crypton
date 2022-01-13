import json
from typing import Optional, Type, Callable, NoReturn, Any

from django.conf import settings
from django.core.cache import caches
from django.db.models import Model
from django.utils.version import PY36

class class_property(property):
    def __get__(self, obj: Any, objtype: Optional[Type[Any]] = None) -> Any:
        return super().__get__(objtype)

class cached_property:  # pragma: no-cover
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.
    """

    name = None

    @staticmethod
    def func(instance: "Model") -> NoReturn:
        raise TypeError("Cannot use cached_property instance without calling __set_name__() on it.")

    @staticmethod
    def _is_mangled(name: str) -> bool:
        return name.startswith("__") and not name.endswith("__")

    def __init__(self, func: Callable, name: Optional[str] = None):
        name = name or func.__name__
        if not (isinstance(name, str) and name.isidentifier()):
            raise ValueError(f"{name} can't be used as the name of a cached_property.")
        if PY36:
            self.real_func = func
        else:
            if self._is_mangled(name):
                raise ValueError(
                    "cached_property does not work with mangled methods on "
                    "Python < 3.6 without the appropriate `name` argument."
                )
            self.name = name
            self.func = func
        self.__doc__ = getattr(func, "__doc__")

    def __set_name__(self, owner: "Model", name: str) -> None:
        if self.name is None:
            self.name = name
            self.func = self.real_func
        elif name != self.name:
            raise TypeError(
                "Cannot assign the same cached_property to two different names "
                f"({repr(self.name)} and {repr(name)})."
            )

    def __get__(self, instance: "Model", cls: Optional[Type["Model"]] = None) -> Any:
        # if settings.RUNLEVEL.is_testing():
        #     if instance is None:
        #         return self
        #     return self.func(instance)
        cache = caches[settings.LRU_CACHE]
        if instance is None:
            return self
        if cls is None:
            cls = instance.__class__
        cls.add_cache_key(self.name)
        cache_key = f"{instance.cache_key}.{self.name}"
        cached = cache.get(cache_key)
        if cached:
            return json.loads(cached)
        value = self.func(instance)
        cache.set(cache_key, json.dumps(value), timeout=None)
        return value