USER algumnome

FROM python:3.12-slim

#ENV PASSWORD=supersecret123
#ARG API_KEY=abc123xyz

COPY app.py /app/app.py
COPY requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
#RUN apt-get install && rm -rf /var/lib/apt/lists/* -y curl

WORKDIR /app

EXPOSE 88
EXPOSE 8080

HEALTHCHECK CMD curl -f http://localhost/ || exit 1

CMD ["python", "app.py"]
