"""Test the image classifier unit methods"""
import numpy as np
import pytest
from PIL import Image

from api.server import config
from api.utils.image_classifier import ImageClassifier
from api.utils.image_classifier import TransferLearningModel
from tests import conftest

#################### Fixtures ####################


@pytest.fixture
def np_dog_image() -> np.ndarray:
    return (
        np.array(
            Image.open(conftest.TEST_DOG_IMAGE_FILE_PATH).resize(
                (config.Config.IMAGE_RESOLUTION, config.Config.IMAGE_RESOLUTION),
            ),
        )
        / 255.0
    )


@pytest.fixture
def np_cat_image() -> np.ndarray:
    return (
        np.array(
            Image.open(conftest.TEST_CAT_IMAGE_FILE_PATH).resize(
                (config.Config.IMAGE_RESOLUTION, config.Config.IMAGE_RESOLUTION),
            ),
        )
        / 255.0
    )


@pytest.fixture
def transfer_learning_model() -> TransferLearningModel:
    return TransferLearningModel()


@pytest.fixture
def image_classifier(transfer_learning_model: TransferLearningModel) -> ImageClassifier:
    return ImageClassifier(
        prediction_model=transfer_learning_model,
    )


#################### Test Classes ####################


class TestTransferLearningModel:
    def test_predict(
        self,
        transfer_learning_model: TransferLearningModel,
        np_dog_image: np.ndarray,
        np_cat_image: np.ndarray,
    ) -> None:
        assert config.ClassNames.dog.name == transfer_learning_model.predict(image_batch=np_dog_image[np.newaxis, ...])
        assert config.ClassNames.cat.name == transfer_learning_model.predict(image_batch=np_cat_image[np.newaxis, ...])


class TestImageClassifier:
    def test_create_scaled_np_array(self, image_classifier: ImageClassifier) -> None:
        with open(conftest.TEST_DOG_IMAGE_FILE_PATH, "rb") as f:
            np_image: np.ndarray = image_classifier.create_scaled_np_array(image=f.read())

        assert np_image.shape == (config.Config.IMAGE_RESOLUTION, config.Config.IMAGE_RESOLUTION, 3)
        assert np.max(np_image) <= 1.0
        assert np.min(np_image) >= 0.0

    def test_process_image(self, image_classifier: ImageClassifier) -> None:
        with open(conftest.TEST_DOG_IMAGE_FILE_PATH, "rb") as f:
            np_image_batch: np.ndarray = image_classifier.create_scaled_image_batch(image=f.read())

        assert np_image_batch.shape == (1, config.Config.IMAGE_RESOLUTION, config.Config.IMAGE_RESOLUTION, 3)
        assert np.max(np_image_batch) <= 1.0
        assert np.min(np_image_batch) >= 0.0
