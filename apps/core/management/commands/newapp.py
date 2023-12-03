from os import path, mkdir
from shutil import rmtree

from django.core.management.base import BaseCommand

from library_backend.settings import BASE_DIR


class Command(BaseCommand):
    help = 'For creating new django app'

    def add_arguments(self, parser):
        # take app name
        parser.add_argument('app_name', type=str, help='Enter App name')

    def handle(self, *args, **options):
        app_name = options['app_name']
        app_name_capitalize = "".join([name.capitalize() for name in app_name.split("_")])

        base_dir = path.join(BASE_DIR, "apis", app_name)

        if path.exists(base_dir):
            # ask user if he wants to overwrite the app
            # if yes, delete the app and create new one
            # if no, exit
            self.stdout.write(self.style.ERROR(f"{app_name} app already exists"))
            # get user input
            user_input = input("Do you want to overwrite the app? (y/n): ")
            if user_input == "y":
                self.stdout.write(self.style.SUCCESS(f"Deleting {app_name} app"))
                # delete app recursively
                rmtree(base_dir)

        # create app folder
        if not path.exists(base_dir):

            self.stdout.write(self.style.SUCCESS(f"Creating {app_name} app"))
            mkdir(base_dir)

            # create app folder structure
            self.stdout.write(self.style.SUCCESS(f"Creating {app_name} app structure"))
            mkdir(path.join(base_dir, "migrations"))

            # create app files
            self.stdout.write(self.style.SUCCESS(f"Creating {app_name} app files"))
            with open(path.join(base_dir, "__init__.py"), "w") as f:
                f.write("")
            with open(path.join(base_dir, "admin.py"), "w") as f:
                f.write("from django.contrib import admin \n\n")

            with open(path.join(base_dir, "apps.py"), "w") as f:
                f.write(f"from django.apps import AppConfig \n\n\n")
                f.write(f"class {app_name_capitalize}Config(AppConfig): \n")
                f.write(f"    default_auto_field = 'django.db.models.BigAutoField' \n")
                f.write(f"    name = 'apps.{app_name}' \n")
                f.write(f"    verbose_name = '{app_name_capitalize}' \n")

            with open(path.join(base_dir, "models.py"), "w") as f:
                f.write("from django.db import models\n")
                f.write("from jupiter.models import TimestampedModel\n\n")
                f.write(f"class {app_name_capitalize}(TimestampedModel): \n")
                f.write(f"    pass \n")

            with open(path.join(base_dir, "serializers.py"), "w") as f:
                f.write("from rest_framework import serializers \n\n")
                f.write(f"from apps.{app_name}.models import {app_name_capitalize} \n\n")
                f.write(f"class {app_name_capitalize}Serializer(serializers.ModelSerializer): \n")
                f.write(f"    class Meta: \n")
                f.write(f"        model = {app_name_capitalize} \n")
                f.write(f"        fields = '__all__' \n")

            with open(path.join(base_dir, "tests.py"), "w") as f:
                f.write("from django.test import TestCase \n\n")

            with open(path.join(base_dir, "urls.py"), "w") as f:
                f.write("from django.urls import path \n\n")
                f.write(f"from apps.{app_name}.views import {app_name_capitalize}View \n\n")
                f.write("urlpatterns = [ \n")
                f.write(f"    path('', {app_name_capitalize}View.as_view(), name='list'), \n")
                f.write(f"    path('<int:pk>/', {app_name_capitalize}View.as_view(), name='details'), \n")
                f.write(f"] \n")

            with open(path.join(base_dir, "views.py"), "w") as f:
                f.write(f"from apps.{app_name}.models import {app_name_capitalize} \n")
                f.write(f"from apps.{app_name}.serializers import {app_name_capitalize}Serializer \n")
                f.write("from jupiter.utils import ApiBaseView \n\n")
                f.write(f"class {app_name_capitalize}View(ApiBaseView): \n")
                f.write(f"    class Meta: \n")
                f.write(f"        model = {app_name_capitalize} \n")
                f.write(f"        serializer = {app_name_capitalize}Serializer \n")

            self.stdout.write(self.style.SUCCESS(f"{app_name} app created successfully"))


        else:
            self.stdout.write(self.style.ERROR(f"{app_name} app already exists"))

        self.stdout.write(self.style.WARNING("Done. Don't forget to add app to INSTALLED_APPS in settings.py"))
