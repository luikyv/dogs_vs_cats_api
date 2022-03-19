"""Test the image classifier methods end to end"""
import pytest

from api.server import config
from api.utils.image_classifier import ImageClassifier
from api.utils.image_classifier import TransferLearningModel
from tests import conftest

#################### Fixtures ####################


@pytest.fixture
def transfer_learning_model() -> TransferLearningModel:
    return TransferLearningModel()


@pytest.fixture
def image_classifier(transfer_learning_model: TransferLearningModel) -> ImageClassifier:
    return ImageClassifier(
        prediction_model=transfer_learning_model,
    )


#################### Test Classes ####################


class TestImageClassifier:
    def test_predict(self, image_classifier: ImageClassifier) -> None:

        with open(conftest.TEST_DOG_IMAGE_FILE_PATH, "rb") as f:
            prediction: str = image_classifier.predict(image=f.read())
        assert prediction == config.ClassNames.dog.name

        with open(conftest.TEST_CAT_IMAGE_FILE_PATH, "rb") as f:
            prediction: str = image_classifier.predict(image=f.read())
        assert prediction == config.ClassNames.cat.name
