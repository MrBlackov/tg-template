from sqlalchemy.ext.asyncio import AsyncSession

from app.logging.base import botlog
from app.db.dao.models import DAO

class BaseLogic:
    def __init__(self, tg_id: int, session: AsyncSession | None = None, **kwargs):
        self.tg_id = tg_id
        self.dao = DAO(session) if session else None
