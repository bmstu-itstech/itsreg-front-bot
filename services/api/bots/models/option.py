from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Option")


@_attrs_define
class Option:
    """Опция для блока с выбором ответа. Представлена в telegram как кнопка в клавиатуре (ReplyKeyboard).

    Attributes:
        text (str): Текст на кнопке. Example: Опция А.
        next_ (int): Состояние (state) следующего блока, если пользователь выбрал данную опцию. Example: 2.
    """

    text: str
    next_: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        text = self.text

        next_ = self.next_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "text": text,
                "next": next_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        text = d.pop("text")

        next_ = d.pop("next")

        option = cls(
            text=text,
            next_=next_,
        )

        option.additional_properties = d
        return option

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
