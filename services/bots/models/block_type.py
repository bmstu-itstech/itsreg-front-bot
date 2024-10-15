from enum import Enum


class BlockType(str, Enum):
    MESSAGE = "message"
    QUESTION = "question"
    SELECTION = "selection"

    def __str__(self) -> str:
        return str(self.value)
