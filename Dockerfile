FROM python:3.11-alpine

WORKDIR /app/solbot
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]