from .base import tg_id, to_json, is_reply, is_admin, is_delay, key, value

class Optionals:
    tg_id = tg_id
    to_json = to_json
    is_reply = is_reply
    is_admin = is_admin
    is_delay = is_delay

class Requireds:
    key = key
    value = value

base_args = [Optionals.tg_id, Optionals.to_json, Optionals.is_reply, Optionals.is_admin, Optionals.is_delay]
