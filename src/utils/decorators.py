from typing import Optional, Type, Any


class class_property(property):
    def __get__(self, obj: Any, objtype: Optional[Type[Any]] = None) -> Any:
        return super().__get__(objtype)
