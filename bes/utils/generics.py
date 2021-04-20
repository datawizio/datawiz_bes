from functools import cached_property
from typing import TypeVar, Generic, List, Iterable, Optional, Any

from pydantic.generics import GenericModel

TList = TypeVar("TList")


class ListGenericModel(GenericModel, Generic[TList]):
    """
    Examples:
        # Class Item with different values
        class Item:
            ...

        # ListGenericModel with item of class Item
        class ListOfItem(ListGenericModel[Item])
            ...

    """
    __root__: List[TList]

    def __init__(self, __root__: List[TList] = None, **data):
        __root__ = __root__ or []
        super().__init__(__root__=__root__, **data)

    def __iter__(self) -> Iterable[TList]:
        return iter(self.__root__)

    def __getitem__(self, item) -> TList:
        return self.__root__[item]

    def __add__(self, other):
        __root__ = self.__root__ + other.__root__
        return self.__class__(__root__=__root__)

    @staticmethod
    def _is_suit(obj: TList, **filters):
        return all(
            (value(getattr(obj, key, None)) if callable(value) else getattr(obj, key, None) == value)
            for key, value in filters.items()
        )

    def filter(self, **filters):
        return self.__class__(__root__=[obj for obj in self.__root__ if self._is_suit(obj, **filters)])

    def exclude(self, **filters):
        return self.__class__(__root__=[obj for obj in self.__root__ if not self._is_suit(obj, **filters)])

    def find(self, **filters) -> Optional[TList]:
        data = self.filter(**filters)
        return data[0] if data else None

    def first(self) -> Optional[TList]:
        return self.__root__[0] if self.__root__ else None

    def values_list(self, *keys: str, flat: bool = False) -> List[Any]:
        assert len(keys) == 1 or (len(keys) > 1 and flat is False), '`flat` option cannot be used with more than 2 keys'
        return [tuple(getattr(o, key, None) for key in keys) if not flat else getattr(o, keys[0], None) for o in self]

    class Config:
        arbitrary_types_allowed = True
        keep_untouched = (cached_property,)


TObject = TypeVar("TObject")


class ObjectGenericModel(GenericModel, Generic[TObject]):
    """
    Examples:
        # Class like type of str, when why need add some methods
        class Path(ObjectGenericModel[str]):
            def to_query():
                ...

        # Use Path instead of str, like a field in another class
        class Terminal(BaseModel):
            path: Path

    """
    __root__: TObject

    def __init__(self, __root__: TObject = None, **data):
        super().__init__(__root__=__root__, **data)

