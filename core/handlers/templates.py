from services.bots.models.post_bots import PostBots
from services.bots.models.entry_point import EntryPoint
from services.bots.models.block import Block, BlockType
from services.bots.models.option import Option


def individual_registration_bot(
        bot_name: str,
        bot_token: str,
        bot_title: str,
        m_greet_text: str,
        q_name_text: str,
        q_group_text: str,
        q_approve_text: str,
        s_approve_yes_text: str,
        s_approve_no_text: str,
        m_finish_text: str,
) -> PostBots:
    blocks = [
        Block(type=BlockType.MESSAGE,   state=1, next_state=2, title="Приветствие",   text=m_greet_text),
        Block(type=BlockType.QUESTION,  state=2, next_state=3, title="ФИО",           text=q_name_text ),
        Block(type=BlockType.QUESTION,  state=3, next_state=4, title="Группа",        text=q_group_text),
        Block(type=BlockType.SELECTION, state=4, next_state=4, title="Подтверждение", text=q_approve_text, options=[
            Option(text=s_approve_yes_text, next_=5),
            Option(text=s_approve_no_text,  next_=2),
        ]),
        Block(type=BlockType.MESSAGE, state=5, next_state=0, title="Конец", text=m_finish_text),
    ]
    entries = [
        EntryPoint(key="start", state=1)
    ]
    mailings = []
    return PostBots(
        bot_uuid=bot_name,
        name=bot_title,
        token=bot_token,
        entries=entries,
        blocks=blocks,
        mailings=mailings,
    )
