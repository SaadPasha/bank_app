FROM python:3.10-slim-bullseye
ENV TZ=Europe/Tallinn
WORKDIR /bank_grpc

RUN pip install grpcio==1.46.0 grpcio-tools==1.46.0

COPY bank_grpc/ /bank_grpc/bank_grpc

EXPOSE 8000
ENTRYPOINT ["python", "bank_grpc/bank_server.py"]
