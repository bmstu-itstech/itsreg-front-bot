from enum import Enum


class BotStatus(str, Enum):
    FAILED = "failed"
    STARTED = "started"
    STOPPED = "stopped"

    def __str__(self) -> str:
        return str(self.value)
