from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [
    path('create', createUser,name='userCreate'),
    path('deposit', depositMoney,name='depositMoney'),
    path('withdraw', withdrawCash,name='withdrawCash'),
    path('transfer_funds', transferFunds,name='transferFunds'),
    path('transaction_record/<int:user_id>', transactionHistory,name='transactionHistory'),
]