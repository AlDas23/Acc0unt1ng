FROM python:slim

WORKDIR /backend
COPY . .
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt

EXPOSE 5050

CMD ["python", "run.py"]