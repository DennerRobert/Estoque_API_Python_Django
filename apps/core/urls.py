from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from apps.core.views import index
import apps.core

urlpatterns = [
     path('', index, name="index"),
]
