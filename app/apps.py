from django.apps import AppConfig


class AppConfig(AppConfig):  # pylint: disable=function-redefined
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
