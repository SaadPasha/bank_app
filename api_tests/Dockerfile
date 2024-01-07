FROM python:3.10-slim-bullseye
ENV TZ=Europe/Tallinn

WORKDIR /api_tests

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["python3", "-m", "pytest", "-v", "api_tests/tests"]