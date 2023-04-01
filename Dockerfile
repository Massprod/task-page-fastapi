FROM python:alpine

WORKDIR /task_page_fastapi

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000/tcp

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]