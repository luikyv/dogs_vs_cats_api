FROM python:3.9-buster AS builder

WORKDIR /pip-packages/
RUN pip3 install poetry==1.1.13
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --without-hashes --output requirements.txt
RUN pip3 download -r requirements.txt
RUN rm pyproject.toml poetry.lock requirements.txt


FROM python:3.9-buster AS prod

WORKDIR /pip-packages/
COPY --from=builder /pip-packages/ /pip-packages/
RUN pip3 install --no-index --find-links=/pip-packages/ /pip-packages/*

WORKDIR /dogs_vs_cats_api/
COPY . /dogs_vs_cats_api/
CMD uvicorn api.server.main:api --reload --port 8000
