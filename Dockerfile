FROM python:3.12-slim

WORKDIR /pudink

RUN pip install pdm

COPY pyproject.toml pdm.lock ./
COPY README.md ./
COPY src/pudink/server ./src/pudink/server
COPY src/pudink/common ./src/pudink/common

RUN pdm install

EXPOSE 8000

# Specify the command to run the application
CMD ["pdm", "run", "server"]
