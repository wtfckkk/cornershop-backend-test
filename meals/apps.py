from django.apps import AppConfig
from django.db.models.signals import post_save
from .signals import create_auth_token


class Config(AppConfig):
    name = 'meals'
    verbose_name = "Meals"

    def ready(self):
        from django.contrib.auth.models import User
        post_save.connect(create_auth_token, sender=User)
