from app.logging.base import botlog

class BaseLogic:
    def __init__(self, tg_id: int, **kwargs):
        self.tg_id = tg_id
