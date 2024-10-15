from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EntryPoint")


@_attrs_define
class EntryPoint:
    """Точка входа для бота. Бот должен иметь как минимум точку входа "start". Иные точки входа используются для создания
    рассылок. Точка входа начинает скрипт бота с отправки блока с состоянием state пользователю.

        Attributes:
            key (str): Уникальный ключ точки входа бота. Example: start.
            state (int): Состояние (state) первого блока в скрипте. Example: 1.
    """

    key: str
    state: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        key = self.key

        state = self.state

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "state": state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key")

        state = d.pop("state")

        entry_point = cls(
            key=key,
            state=state,
        )

        entry_point.additional_properties = d
        return entry_point

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
