import enum
from pathlib import Path
from typing import Literal


class ClassNames(enum.Enum):
    dog = 1
    cat = 0


class Config:
    """API configurations"""

    IMAGE_RESOLUTION: int = 224
    SAVED_MODEL_PATH: str = str(Path(__file__).parent.parent.parent.absolute()) + "/model"
    CLASS_NAMES_LITERAL = Literal[tuple(cn.name for cn in ClassNames)]  # type: ignore