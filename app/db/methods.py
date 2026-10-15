from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dao.models import DAO, TgUserDB
from app.db.connection import connection

@connection()
async def check_user(session: AsyncSession, tg_id: int, username: str | None, fullname: str | None, **kwargs):
        dao = DAO(session)
        user = await dao.user.query_by_tg_id(tg_id)
        if user:
            if username:
                user.tg_user.username = username
            if fullname:
                user.tg_user.fullname = fullname
        else: 
            user = await dao.user.add({'tg_id':tg_id})
            user.tg_user = TgUserDB(tg_id=tg_id, username=username, fullname=fullname)
        return user