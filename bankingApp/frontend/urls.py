from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('register/', register,name="register"),
    path('success/', success_view,name="success"),
]
