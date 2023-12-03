from django.http import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.urls import reverse


def is_superuser_or_staff(user):
    return user.is_superuser or user.is_staff



def is_superadmin(user):
    return user.is_superuser