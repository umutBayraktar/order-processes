from django.db import models
from manage import init_django
from django.contrib.auth.models import User

init_django()


class Restaurant(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name
