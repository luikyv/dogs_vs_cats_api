"""Test the API endpoints end to end"""
from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from api import config
from api.server.main import api
from tests import conftest

#################### Fixtures ####################


@pytest.fixture
def api_client() -> TestClient:
    return TestClient(api)


#################### Test Classes ####################


class TestClassifyCatAndDogs:
    """Test the post endpoint to classify images in either cats or dogs"""

    endpoint_url: str = "/classifier/cats-and-dogs"

    def test_invalid_extension(self, api_client: TestClient) -> None:

        with open(conftest.TEST_DOG_IMAGE_FILE_PATH, "rb") as f:
            resp = api_client.post(self.endpoint_url, files={"picture": ("picture.invalid_extension", f)})

        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "invalid extension" in resp.json()["detail"].lower()

    def test_successful(self, api_client: TestClient) -> None:

        ### Classify a dog image ###
        with open(conftest.TEST_DOG_IMAGE_FILE_PATH, "rb") as f:
            resp = api_client.post(self.endpoint_url, files={"picture": ("picture.jpeg", f, "image/jpeg")})

        assert resp.status_code == status.HTTP_200_OK
        resp_json: dict[str, Any] = resp.json()
        assert resp_json["predicted_class"] == config.ClassNames.dog.name

        ### Classify a cat image ###
        with open(conftest.TEST_CAT_IMAGE_FILE_PATH, "rb") as f:
            resp = api_client.post(self.endpoint_url, files={"picture": ("picture.jpeg", f, "image/jpeg")})

        assert resp.status_code == status.HTTP_200_OK
        resp_json: dict[str, Any] = resp.json()
        assert resp_json["predicted_class"] == config.ClassNames.cat.name
