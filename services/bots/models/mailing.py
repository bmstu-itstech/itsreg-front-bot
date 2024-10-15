from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Mailing")


@_attrs_define
class Mailing:
    """Рассылка от бота. При старте рассылки активирует точку входа с ключом entryKey всем пользователям, прошедшим блок с
    состоянием requiredState.

        Attributes:
            name (str): Имя рассылки. Example: Рассылка для завершивших скрипт бота..
            entry_key (str): Ключ точки входа (EntryPoint), которая активируется при старте рассылки. Example: mailing-1.
            required_state (int): Состояние (state) блока, требуемого для отправки рассылки или 0, для всех, кто завершил
                скрипт. Так, requiredState = 5 обозначает, что рассылка будет отправлена всем участникам, которые ответили на
                блок с состоянием 5.
    """

    name: str
    entry_key: str
    required_state: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        entry_key = self.entry_key

        required_state = self.required_state

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "entryKey": entry_key,
                "requiredState": required_state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        entry_key = d.pop("entryKey")

        required_state = d.pop("requiredState")

        mailing = cls(
            name=name,
            entry_key=entry_key,
            required_state=required_state,
        )

        mailing.additional_properties = d
        return mailing

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
