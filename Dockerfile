FROM python:alpine

LABEL authors="Massprod"

WORKDIR /task-page-fastapi

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5050:5050/tcp

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5050"]