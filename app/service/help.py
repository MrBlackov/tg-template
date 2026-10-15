from app.service.base import BaseService, AnswerBody
from app.tg.text.help import HelpText

class HelpService(BaseService):
    text = HelpText

    async def main(self):
        return await self.answer([
            AnswerBody(text=self.text.main())
            ])
