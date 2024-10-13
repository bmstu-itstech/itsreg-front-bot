import time
from typing import List

import jwt
import requests

from common.functions import generate_token
from common.models.block import Block
from common.models.entry_point import EntryPoint
from config import load_config


config = load_config("config.ini")


class ItsRegApi:
    def __init__(self, chat_id: int, token: str | None = None, base_url="http://localhost:8400/api/"):
        if not token:
            self.token = generate_token(chat_id)
        else:
            self.token = token
        self.chat_id = chat_id
        self.base_url = base_url
        self.session = requests.session()
        self.session.headers = {"Authorization": f"Bearer {self.token}"}

    def get(self, url, params=None):
        res = self.session.get(self.base_url + url, params=params)
        if res.status_code == 401:
            self.token = generate_token(self.chat_id)
            self.session.headers = {"Authorization": f"Bearer {self.token}"}
        res = self.session.get(self.base_url + url, params=params)
        return res.json()

    def put(self, url, data=None):
        res = self.session.put(self.base_url + url, json=data)
        if res.status_code == 401:
            self.token = generate_token(self.chat_id)
            self.session.headers = {"Authorization": f"Bearer {self.token}"}
        res = self.session.put(self.base_url + url, json=data)
        return res

    def post(self, url, data=None):
        res = self.session.post(self.base_url + url, json=data)
        if res.status_code == 401:
            self.token = generate_token(self.chat_id)
            self.session.headers = {"Authorization": f"Bearer {self.token}"}
        res = self.session.post(self.base_url + url, json=data)
        return res

    def create_bot(
        self,
        uuid: str,
        name: str,
        token: str,
        entries: List[EntryPoint],
        blocks: List[Block],
    ):
        data = {
            "botUUID": uuid,
            "name": name,
            "token": token,
            "entries": [entry_point.__dict__ for entry_point in entries],
            "blocks": [block.__dict__() for block in blocks],
        }
        return self.put("bots", data)

    def get_bots(self):
        return self.get("bots")
