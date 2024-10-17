from services.bots.api.default import get_bots
from services.bots.models import BotStatus


def get_bot_repr(bot_obj: get_bots.Bot) -> str:
    return (
        f"<i>Название:</i> {bot_obj.name}\n"
        f"<i>Ссылка:</i> https://t.me/{bot_obj.bot_uuid}\n"
        f"<i>Состояние</i>: <b>{'запущен' if bot_obj.status == BotStatus.STARTED else 'остановлен'}</b>"
    )
