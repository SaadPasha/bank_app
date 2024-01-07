FROM python:3.10-slim-bullseye
WORKDIR /fast_api
ENV PYTHONPATH=/fast_api

RUN pip install fastapi uvicorn email-validator grpcio==1.46.0 grpcio-tools==1.46.0

COPY fast_api /fast_api

COPY bank_grpc /fast_api/bank_grpc

ENV PYTHONPATH=/fast_api:/fast_api/bank_grpc

WORKDIR /fast_api


EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
