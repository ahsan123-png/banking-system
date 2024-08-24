from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('register/', register,name="register"),
    path('money/deposit', deposit_money_view,name="depositMoney"),
    path('money/withdrawal', withdraw_money_view,name="withdrawMoney"),
    path('online_transaction', onlineTransaction,name="onlineTransaction"),
    path('success/', success_view,name="success"),
    path('home/', index,name="index"),
]
