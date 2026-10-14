from app.tg.callback.base import BackCall, BaseCall

class MainCall(BaseCall, prefix='main'):
    pass

class MyStateCall(MainCall, prefix='my_state'):
    pass