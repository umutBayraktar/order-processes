#!/usr/bin/env python
import os
import dotenv
from pathlib import Path


def init_django():
    dotenv.read_dotenv()
    import django
    from django.conf import settings

    if settings.configured:
        return

    BASE_DIR = Path(__file__).resolve().parent.parent
    #DATABASE_DIR = os.path.join(BASE_DIR, "order-list", "orderlist")
    DATABASE_PATH = os.path.join(BASE_DIR, "db.sqlite3")
    DATABASE_FILE = os.environ.get("DATABASE_FILE", DATABASE_PATH)

    settings.configure(
        RABBITMQ_HOST=os.environ.get('RABBITMQ_HOST', 'localhost'),
        RABBITMQ_VIRTUALHOST=os.environ.get('RABBITMQ_VIRTUALHOST', '/'),
        RABBITMQ_PORT=os.environ.get('RABBITMQ_PORT', 5672),
        RABBITMQ_USER=os.environ.get('RABBITMQ_USER', 'guest'),
        RABBITMQ_PASSWORD=os.environ.get('RABBITMQ_PASSWORD', 'guest'),
        QUEUE_NAME=os.environ.get('QUEUE_NAME', 'orders'),
        DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'restaurant',
            'food',
            'order',
            'rabbitmq',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': DATABASE_PATH,
            }
        },
        ALLOWED_HOSTS=['*'],
        DEBUG=os.environ.get('DEBUG', True),
    )
    django.setup()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    init_django()
    execute_from_command_line()
