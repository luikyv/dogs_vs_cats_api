"""Interfaces"""
import abc

import numpy as np

from .. import config

#################### Interfaces ####################


class PredictionModel(abc.ABC):
    @abc.abstractmethod
    def predict(self, image_batch: np.ndarray) -> config.ClassNames:
        """Make a prediction on a batch of one image with shape (IMAGE_RESOLUTION, IMAGE_RESOLUTION, 3)"""
        ...
