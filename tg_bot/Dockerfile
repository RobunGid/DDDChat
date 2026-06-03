FROM python:3.14.5-slim-trixie as builder

COPY poetry.lock pyproject.toml ./

RUN python -m pip install poetry==2.3.4 poetry-plugin-export && \
    poetry export -o requirements.prod.txt --without-hashes && \
    poetry export --with=dev -o requirements.dev.txt --without-hashes

FROM python:3.14.5-slim-trixie as dev

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY --from=builder requirements.dev.txt /app

RUN apt update -y && \
	apt install -y python3-dev \
	gcc \
	musl-dev && \
	pip install --upgrade pip && pip install --no-cache-dir -r requirements.dev.txt
	
COPY /tg_bot/ /app

EXPOSE 8000