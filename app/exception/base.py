from typing import Literal   
from app.logging.base import botlog

class PythonError:
    msg = '⚠️ Непредвиденная ошибка'

class BotError(Exception):
    msg = 'Базовый класс ошибки'
    faq = ''
    emodzi = '❌'

    def __init__(self, *args, level: Literal['trace', 'debug', 'info', 'success', 'warning', 'error', 'critical'] = 'warning', is_error: bool = True, **kwargs):
        self.level = level
        self.args = args
        self.kwargs = kwargs
        self.is_error = is_error
        if is_error:
            super().__init__(*args)
            getattr(botlog.logger, level)(f'{self.__class__.__name__}, msg: {' '.join(self.args) if len(args) > 0 else self.msg}, kwargs: {self.kwargs}')

    def __str__(self):
        return super().__str__()
    
    @property
    def to_msg(self):
        return f'{self.emodzi} {self.name}: {self.msg}'
     
    @property
    def name(self):
        return self.__class__.__name__

class PermissionError(BotError):
    msg = 'У вас нет доступа'
    emodzi = '❌'

class ALienCallbackError(BotError):
    msg = 'Это не ваша кнопка'
    emodzi = '❌'
