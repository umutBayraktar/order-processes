# syntax=docker/dockerfile:1
FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./orderlist/ /code/orderlist/
WORKDIR /code/orderlist/
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]