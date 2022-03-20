"""Schemas"""
from pydantic import BaseModel
from pydantic import Field

from . import config

#################### Schemas ####################


class CatsAndDogsClassifierResponse(BaseModel):
    predicted_class: config.Config.CLASS_NAMES_LITERAL = Field(..., description="The most probable label")
