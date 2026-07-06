FROM python:3.10

WORKDIR /code

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "7860"]