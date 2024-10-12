import logging

import time
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.db.models import User, ItsBot


logger = logging.getLogger(__name__)


class Repo:
    """Db abstraction layer"""

    def __init__(self, conn):
        self.conn: AsyncSession = conn

    async def add_user(self, uuid: int):
        db_user = await self.get_user(uuid)
        if db_user is not None:
            return

        user = User(
            uuid=uuid,
            pseudo_password=str(int(time.time())),
        )
        self.conn.add(user)
        await self.conn.commit()

    async def get_user(self, uuid: int) -> User | None:
        res = await self.conn.execute(
            select(User).where(User.uuid == uuid)
        )
        
        return res.scalars().first()

    async def get_users(self) -> list[User]:
        res = await self.conn.execute(
            select(User)
        )

        return res.scalars().all()

    async def update_user(self, uuid: int, **kwargs):
        user = await self.get_user(uuid)

        if not user:
            raise ValueError(f'User with {uuid=} doesn\'t exist')

        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise ValueError(f'Class `User` doesn\'t have argument {key}') 
            setattr(user, key, value)
        await self.conn.commit()

    async def add_itsbot(self, token: str, uuid: str, name: str):
        itsbot = ItsBot(
            token=token,
            uuid=uuid,
            name=name,
        )
        self.conn.add(itsbot)
        await self.conn.commit()

    async def get_bots(self) -> list[ItsBot]:
        res = await self.conn.execute(
            select(ItsBot)
        )

        return res.scalars().all()
