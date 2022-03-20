import io

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image

from .. import config
from .interfaces import PredictionModel

#################### Machine Learning Approaches ####################


class TransferLearningModel(PredictionModel):
    def __init__(self) -> None:
        self.saved_model = tf.keras.models.load_model(
            config.Config.SAVED_MODEL_PATH,
            custom_objects={"KerasLayer": hub.KerasLayer},
        )

    def predict(self, image_batch: np.ndarray) -> config.Config.CLASS_NAMES_LITERAL:
        """Make a prediction on a batch of one image with shape (IMAGE_RESOLUTION, IMAGE_RESOLUTION, 3)"""
        predictions = self.saved_model.predict(image_batch)
        most_probable_idx: np.intp = np.argmax(predictions, axis=-1)[0]
        return config.ClassNames(int(most_probable_idx)).name


#################### Main class ####################


class ImageClassifier:
    def __init__(self, prediction_model: PredictionModel) -> None:
        self.prediction_model = prediction_model

    def _create_scaled_np_array(self, image: bytes) -> np.ndarray:
        """Convert the image in bytes to a numpy array scaled by a factor of 255"""

        return (
            np.array(
                Image.open(io.BytesIO(image)).resize((config.Config.IMAGE_RESOLUTION, config.Config.IMAGE_RESOLUTION)),
            )
            / 255.0
        )

    def _create_scaled_image_batch(self, image: bytes) -> np.ndarray:
        """Convert the image in bytes to a valid input to the prediction model"""
        np_image: np.ndarray = self._create_scaled_np_array(image=image)
        # Add one more dimension to the array to simulate a batch of one image
        return np_image[np.newaxis, ...]

    def predict(self, image: bytes) -> config.Config.CLASS_NAMES_LITERAL:

        image_batch: np.ndarray = self._create_scaled_image_batch(image=image)
        return self.prediction_model.predict(image_batch=image_batch)
