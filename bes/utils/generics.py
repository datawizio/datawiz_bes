from functools import cached_property
from typing import TypeVar, Generic, List, Iterable, Optional, Any

from pydantic import ConfigDict, RootModel

TList = TypeVar("TList")


class ListGenericModel(RootModel[List[TList]], Generic[TList]):
    """
    Examples:
        # Class Item with different values
        class Item:
            ...

        # ListGenericModel with item of class Item
        class ListOfItem(ListGenericModel[Item])
            ...

    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        ignored_types=(cached_property,),
    )

    def __init__(self, root: List[TList] = None, **data):
        super().__init__(root=root or [], **data)

    def __iter__(self) -> Iterable[TList]:
        return iter(self.root)

    def __getitem__(self, item) -> TList:
        return self.root[item]

    def __add__(self, other):
        root = self.root + other.root
        return self.__class__(root=root)

    def __len__(self) -> int:
        return len(self.root)

    def __bool__(self) -> bool:
        return bool(self.root)

    @staticmethod
    def _is_suit(obj: TList, *args, **filters):
        return obj in args or all(
            (value(getattr(obj, key, None)) if callable(value) else getattr(obj, key, None) == value)
            for key, value in filters.items()
        )

    def filter(self, *args, **filters):
        return self.__class__(root=[obj for obj in self.root if self._is_suit(obj, *args, **filters)])

    def exclude(self, *args, **filters):
        return self.__class__(root=[obj for obj in self.root if not self._is_suit(obj, *args, **filters)])

    def get(self, *args, **filters) -> Optional[TList]:
        data = self.filter(*args, **filters)
        return data[0] if data else None

    def first(self) -> Optional[TList]:
        return self.root[0] if self.root else None

    def values_list(self, *keys: str, flat: bool = False) -> List[Any]:
        assert len(keys) == 1 or (len(keys) > 1 and flat is False), '`flat` option cannot be used with more than 2 keys'
        return [tuple(getattr(o, key, None) for key in keys) if not flat else getattr(o, keys[0], None) for o in self]

    def append(self, obj: TList):
        self.root.append(obj)


TObject = TypeVar("TObject")


class ObjectGenericModel(RootModel[TObject], Generic[TObject]):
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
    def __init__(self, root: TObject = None, **data):
        super().__init__(root=root, **data)

    def __bool__(self) -> bool:
        return bool(self.root)
