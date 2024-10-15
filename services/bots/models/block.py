from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.block_type import BlockType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.option import Option


T = TypeVar("T", bound="Block")


@_attrs_define
class Block:
    """Минимальная структурная единица сценария бота. Представляет из себя сообщение, которое отправляет бот пользователю,
    и в зависимости от типа блока обрабатывается по-разному:
     - Сообщение (message) - просто сообщение от бота. Не ждет ответа пользователя и сразу переключает пользователя на
    следующий блок с состоянием next.
     - Вопрос (question) - сообщение от бот, ожидается ответ пользователя. После ответа пользователя переключает
    пользователя на следующий блок с состоянием next
     - Выбор (selection) - сообщение от бота, после которого ожидается ответ пользователя кнопкой или произвольным
    текстом. Если пользователь отвечает кнопкой, бот переключает его на следующий блок с состоянием next у выбранной
    опции (Option). Если пользователь отвечает произвольным текстом, переключает пользователя на следующий блок с
    состоянием next.

        Attributes:
            type (BlockType): Тип кнопки:
                 - Сообщение (message) - просто сообщение от бота. Не ждет ответа пользователя и сразу переключает пользователя
                на следующий блок с состоянием next.
                 - Вопрос (question) - сообщение от бот, ожидается ответ пользователя. После ответа пользователя переключает
                пользователя на следующий блок с состоянием next
                 - Выбор (selection) - сообщение от бота, после которого ожидается ответ пользователя кнопкой или произвольным
                текстом. Если пользователь отвечает кнопкой, бот переключает его на следующий блок с состоянием next у выбранной
                опции (Option). Если пользователь отвечает произвольным текстом, переключает пользователя на следующий блок с
                состоянием next.
                 Example: message.
            state (int): Уникальный идентификатор блока в рамках бота. Не может равняться нулю. Example: 1.
            next_state (int): Состояние (state) другого блока. Конкретное значение определяется типом (type) блока. Example:
                2.
            title (str): Название блока. Используется в заголовке таблицы с ответами участников. Example: Greeting.
            text (str): Текст сообщения бота. Не допускается использование вёрстки. Example: Hello, user!.
            options (Union[Unset, List['Option']]): Опции для блока с выбором ответа. Не допускается использование опций для
                других типов блока.
    """

    type: BlockType
    state: int
    next_state: int
    title: str
    text: str
    options: Union[Unset, List["Option"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        state = self.state

        next_state = self.next_state

        title = self.title

        text = self.text

        options: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.options, Unset):
            options = []
            for options_item_data in self.options:
                options_item = options_item_data.to_dict()
                options.append(options_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "state": state,
                "nextState": next_state,
                "title": title,
                "text": text,
            }
        )
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.option import Option

        d = src_dict.copy()
        type = BlockType(d.pop("type"))

        state = d.pop("state")

        next_state = d.pop("nextState")

        title = d.pop("title")

        text = d.pop("text")

        options = []
        _options = d.pop("options", UNSET)
        for options_item_data in _options or []:
            options_item = Option.from_dict(options_item_data)

            options.append(options_item)

        block = cls(
            type=type,
            state=state,
            next_state=next_state,
            title=title,
            text=text,
            options=options,
        )

        block.additional_properties = d
        return block

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
