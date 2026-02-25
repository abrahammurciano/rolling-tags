FROM ghcr.io/astral-sh/uv:python3.14-alpine
WORKDIR /code
COPY . /code/
RUN uv sync --frozen
CMD ["uv", "run", "rolling-tags"]