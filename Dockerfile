FROM python:3.12-slim

WORKDIR /pudink

RUN pip install pdm

COPY pyproject.toml pdm.lock ./
COPY README.md ./
COPY server .server
COPY common .common

RUN pdm install

EXPOSE 8000

# Specify the command to run the application
CMD ["pdm", "run", "server"]
