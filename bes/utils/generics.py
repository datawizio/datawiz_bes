from typing import TypeVar, Generic, List, Iterable, Optional

from pydantic.generics import GenericModel

T = TypeVar("T")


class ListGenericModel(GenericModel, Generic[T]):
    __root__: List[T]

    def __init__(self, __root__: List[T] = None, **data):
        __root__ = __root__ or []
        super().__init__(__root__=__root__, **data)

    def __iter__(self) -> Iterable[T]:
        return iter(self.__root__)

    def __getitem__(self, item) -> T:
        return self.__root__[item]

    @staticmethod
    def _is_suit(obj: T, **filters):
        return all(
            (value(getattr(obj, key, None)) if callable(value) else getattr(obj, key, None) == value)
            for key, value in filters.items()
        )

    def filter(self, **filters):
        return self.__class__(__root__=[obj for obj in self.__root__ if self._is_suit(obj, **filters)])

    def exclude(self, **filters):
        return self.__class__(__root__=[obj for obj in self.__root__ if not self._is_suit(obj, **filters)])

    def find(self, **filters) -> Optional[T]:
        data = self.filter(**filters)
        return data[0] if data else None

    def first(self) -> Optional[T]:
        return self.__root__[0] if self.__root__ else None

    class Config:
        arbitrary_types_allowed = True
