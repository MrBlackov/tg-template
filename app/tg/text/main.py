from app.tg.text.base import BaseText

class MainText(BaseText):
    @classmethod
    def state_clear(self):
        return f'✅ Куки очищены'

    @classmethod
    def state_pop(self):
        return f'✅ Кук удален'

    @classmethod
    def state_dont_pop(self):
        return f'❌ Кук не найден'

    @classmethod
    def state(self, data: dict):
        text = self.html.json_format(data, 4)
        return self.html.anchor('start-json') + text.pre('json').details('JSON', text.count('\n') > 10) + self.html('Вверх').href('#start-json')