from common.models.option import Option


class Block:
    def __init__(self, block_type: str, state: int, next_state: int, title: str, text: str, options: list[Option] = None):
        self.block_type = block_type
        self.state = state
        self.next_state = next_state
        self.title = title
        self.text = text
        self.options = options or []

    def __dict__(self):
        data = {
            "type": self.block_type,
            "state": self.state,
            "nextState": self.next_state,
            "title": self.title,
            "text": self.text,
        }
        if self.options:
            data["options"] = [option.__dict__ for option in self.options]
        return data
