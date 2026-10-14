from app.service.base import BaseService, AnswerBody
from app.tg.text.help import HelpText

class HelpService(BaseService):
    def __init__(self, message = None, state = None, callback = None, **kwargs):
        super().__init__(message, state, callback, **kwargs)
        self.text = HelpText

    async def main(self):
        return await self.answer([
            AnswerBody(text=self.text.main())
            ])
