FROM python:3.12
WORKDIR /
COPY req.txt req.txt
RUN pip install -r req.txt
COPY . .