import logging

from common.functions import generate_token

logger = logging.getLogger(__name__)


class Repo:
    """Db abstraction layer"""

    def __init__(self, data):
        self.data: dict[int, str] = data        # dict[<int>chat_id] = <str>token

    def update_user(self, uuid: int, token: str = None):
        """Update user (add if not exists)"""

        context_token = self.get_user_token(uuid)
        if not token and not context_token:
            token = generate_token(uuid)
        self.data[uuid] = token or context_token
        return self.data[uuid]

    def get_user_token(self, uuid: int) -> str | None:
        return self.data.get(uuid, None)
