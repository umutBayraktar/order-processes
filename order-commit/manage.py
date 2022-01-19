#!/usr/bin/env python
from pathlib import Path
import os


def init_django():
    import django
    from django.conf import settings

    if settings.configured:
        return

    BASE_DIR = Path(__file__).resolve().parent.parent
    DATABASE_DIR = os.path.join(BASE_DIR, "order-list", "orderlist")
    DATABASE_PATH = os.path.join(DATABASE_DIR, "db.sqlite3")
    print(DATABASE_PATH)

    settings.configure(

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
        ALLOWED_HOSTS=[],
        DEBUG=True
    )
    django.setup()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    init_django()
    execute_from_command_line()
