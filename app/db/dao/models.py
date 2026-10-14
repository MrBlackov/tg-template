from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, delete, func, join, or_, all_, and_, any_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dao.base import BaseDAO, TgDAO
from app.db.models.main import ChatDB, UserDB, TgChatDB, TgUserDB
from app.db.base import Base

class UserDAO(TgDAO[UserDB]):
    model = UserDB

class ChatDAO(TgDAO[ChatDB]):
    model = ChatDB

class TgChatDAO(TgDAO[TgChatDB]):
    model = TgChatDB

class TgUserDAO(TgDAO[TgUserDB]):
    model = TgUserDB

class DAO:
    def __init__(self, session: AsyncSession):
        if type(session) != AsyncSession:
            raise TypeError('This session is not AsyncSession')
        self.session = session
        self.user = UserDAO(self.session)
        self.chat = ChatDAO(self.session)
        self.tgchat = TgChatDAO(self.session)
        self.tguser = TgUserDAO(self.session)

    async def flush(self):
        await self.session.flush()  

    async def commit(self):
        await self.session.commit()    

    async def close(self):
        await self.session.close()        
        
    async def rollback(self):
        await self.session.rollback()  
