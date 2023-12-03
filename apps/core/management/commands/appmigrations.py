import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        # get all apps name
        from konnect.settings import INSTALLED_APPS

        apps = [app for app in INSTALLED_APPS if app.startswith("apps")]

        apps = [app.split(".")[1] for app in apps]

        # make migrations cmd

        # ("python manage.py makemigrations " + " ".join(apps))

        os.system("python manage.py makemigrations " + " ".join(apps))
