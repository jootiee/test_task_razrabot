FROM python:3.9.21-slim as prod

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src .
CMD ["python", "main.py"]