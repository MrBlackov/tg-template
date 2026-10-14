from pydantic import BaseModel, ConfigDict, Field, field_validator, computed_field
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup

class BaseValidate(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
