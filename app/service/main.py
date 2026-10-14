from app.service.base import BaseService, AnswerBody
from app.logic.main import MainLogic
from app.tg.text.main import MainText
from app.tg.buttons.main import MainIKB

class MainService(BaseService):
    def __init__(self, message = None, state = None, callback = None, **kwargs):
        super().__init__(message, state, callback, **kwargs)
        self.logic = MainLogic(tg_id=self.tg_id)
        self.text = MainText
        self.IKB = MainIKB(tg_id=self.tg_id)
    
    async def my_state(self):
        data = await self.fsm.state.get_data()
        return await self.answer([
            AnswerBody(
                text=self.text.state(data),
                reply_markup=self.IKB.my_state(),
                is_rich_text=True
            )
            ])

    async def my_state_clear(self):
        await self.fsm.state.clear()
        return await self.answer([
            AnswerBody(
                text=self.text.state_clear()
            )
            ])

    async def my_state_pop(self):
        data = await self.fsm.state.get_data()
        key = self.command.args
        if key in data:
            data.pop(key)
            await self.fsm.state.set_data(data)
            text = self.text.state_pop()
        else:
            text = self.text.state_dont_pop()
        return await self.answer([
            AnswerBody(
                text=text
            )
            ])    