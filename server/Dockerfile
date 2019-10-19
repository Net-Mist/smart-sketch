FROM python:3.7-slim
LABEL Noah Yoshida "nyoshida@nd.edu"
RUN apt-get update -y && apt-get install -y gcc libc-dev

COPY requirements.txt /app/requirements.txt
ENV HOME=/app
WORKDIR /app
RUN pip3 install -r requirements.txt

COPY . /app
COPY dist /app

EXPOSE 80
CMD python3 main.py
