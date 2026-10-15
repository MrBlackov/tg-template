import inspect
from typing import Any, Callable
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.utils.deep_linking import create_deep_link, decode_payload
from pydantic import ValidationError

from config import settings

class BaseStartArgs(CallbackData, prefix='start'):

    def url(self):
        return create_deep_link(settings.bot.username, link_type='start', payload=self.pack(), encode=True)

    @classmethod
    def filter(cls, rule: Callable[[Any], Any] | None = None) -> BaseFilter:
        class _StartFilter(BaseFilter):
            async def __call__(self, message: Message) -> bool | dict[str, Any]:
                if not message.text or not message.text.startswith("/start"):
                    return False
                parts = message.text.split(maxsplit=1)
                try:
                    data = cls.unpack(decode_payload(parts[1]))
                except (ValueError, UnicodeDecodeError, IndexError) as e:
                    try:
                        data = cls()
                    except ValidationError as e:
                        return False

                if rule is not None:
                    if not await self._check_rule(rule, data):
                        return False

                args = {k: v for k, v in data.__dict__.items() if not k.startswith("_")}
                return args or True

            @staticmethod
            async def _check_rule(rule, data) -> bool:
                result = rule(data)
                if inspect.isawaitable(result):
                    result = await result
                return bool(result)
        return _StartFilter()

class HelpArg(BaseStartArgs, prefix='help'):
    pass
