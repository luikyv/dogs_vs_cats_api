"""API Endpoints"""
import logging
from typing import Union

import tensorflow as tf
from fastapi import FastAPI
from fastapi import File
from fastapi import HTTPException
from fastapi import Query
from fastapi import status
from fastapi import UploadFile
from fastapi.middleware.cors import CORSMiddleware

from . import dependencies
from .. import config
from .. import schemas

#################### Initialization ####################

api = FastAPI(
    title="Cat and Dogs API",
    description="Classify pictures between cats and dogs",
    version=config.Config.VERSION,
)

logger = tf.get_logger()
logger.setLevel(logging.ERROR)

#################### Middleware ####################

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

#################### Endpoints ####################


@api.post(
    "/classifier/cats-and-dogs",
    response_model=schemas.CatsAndDogsClassifierResponse,
    status_code=status.HTTP_200_OK,
    responses={
        422: {"description": "Could not process the provided picture | The provided picture has an invalid extension"},
    },
)
async def classify(
    picture: UploadFile = File(..., description="Upload the picture of either a cat or a dog")
) -> schemas.CatsAndDogsClassifierResponse:

    extension: str = picture.filename.split(".")[-1]
    if extension not in ["jpg", "jpeg", "png"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The provided picture has an invalid extension",
        )

    image: Union[bytes, str] = await picture.read()
    if not isinstance(image, bytes):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Could not process the provided picture",
        )

    return schemas.CatsAndDogsClassifierResponse(predicted_class=dependencies.image_classifier.predict(image=image))
