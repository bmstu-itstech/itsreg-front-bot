from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.block import Block
    from ..models.entry_point import EntryPoint
    from ..models.mailing import Mailing


T = TypeVar("T", bound="PostBots")


@_attrs_define
class PostBots:
    """Данные, необходимые для создания бота.

    Attributes:
        bot_uuid (str): Уникальный идентификатор бота. Не должен превышать длину в 36 символов. Example: 14ab-d"740".
        name (str): Имя бота. Example: Example bot.
        token (str): Телеграм токен бота. Получить токен можно в телеграм-боте @BotFather.
        entries (List['EntryPoint']): Все точки входа бота, см. EntryPoint. Необходимо наличие точки входа start.
        blocks (List['Block']): Все блоки бота, см. Block.
        mailings (Union[Unset, List['Mailing']]): Все рассылки бота, см. Mailings.
    """

    bot_uuid: str
    name: str
    token: str
    entries: List["EntryPoint"]
    blocks: List["Block"]
    mailings: Union[Unset, List["Mailing"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bot_uuid = self.bot_uuid

        name = self.name

        token = self.token

        entries = []
        for entries_item_data in self.entries:
            entries_item = entries_item_data.to_dict()
            entries.append(entries_item)

        blocks = []
        for blocks_item_data in self.blocks:
            blocks_item = blocks_item_data.to_dict()
            blocks.append(blocks_item)

        mailings: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.mailings, Unset):
            mailings = []
            for mailings_item_data in self.mailings:
                mailings_item = mailings_item_data.to_dict()
                mailings.append(mailings_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "botUUID": bot_uuid,
                "name": name,
                "token": token,
                "entries": entries,
                "blocks": blocks,
            }
        )
        if mailings is not UNSET:
            field_dict["mailings"] = mailings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.block import Block
        from ..models.entry_point import EntryPoint
        from ..models.mailing import Mailing

        d = src_dict.copy()
        bot_uuid = d.pop("botUUID")

        name = d.pop("name")

        token = d.pop("token")

        entries = []
        _entries = d.pop("entries")
        for entries_item_data in _entries:
            entries_item = EntryPoint.from_dict(entries_item_data)

            entries.append(entries_item)

        blocks = []
        _blocks = d.pop("blocks")
        for blocks_item_data in _blocks:
            blocks_item = Block.from_dict(blocks_item_data)

            blocks.append(blocks_item)

        mailings = []
        _mailings = d.pop("mailings", UNSET)
        for mailings_item_data in _mailings or []:
            mailings_item = Mailing.from_dict(mailings_item_data)

            mailings.append(mailings_item)

        post_bots = cls(
            bot_uuid=bot_uuid,
            name=name,
            token=token,
            entries=entries,
            blocks=blocks,
            mailings=mailings,
        )

        post_bots.additional_properties = d
        return post_bots

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
