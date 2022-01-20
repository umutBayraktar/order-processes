# syntax=docker/dockerfile:1
FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./food/ /code/food/
COPY ./order/ /code/order/
COPY ./rabbitmq/ /code/rabbitmq/
COPY ./restaurant/ /code/restaurant/
COPY ./main.py /code/main.py
COPY ./manage.py /code/manage.py
COPY ./.env /code/.env
EXPOSE 8000

CMD ["python", "main.py"]