from decimal import Decimal
import json
from django.shortcuts import render
from django.shortcuts import render, redirect
from .form import CreateUserForm, DepositMoneyForm, TransferFundsForm
import requests
from django.conf import settings
from datetime import date

API_URL='http://127.0.0.1:8000'
#======== front end views =============

#======== register New user ===============
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # Convert cleaned_data to a dictionary
            cleaned_data = form.cleaned_data
            # Convert date fields to strings
            for key, value in cleaned_data.items():
                if isinstance(value, date):
                    cleaned_data[key] = value.isoformat()  # Convert date to ISO format (YYYY-MM-DD)
            response = requests.post(
                'http://127.0.0.1:8000/users/create',
                data=json.dumps(cleaned_data),
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 200:
                return redirect('success')
            else:
                return render(request, 'userCreate.html', {'form': form, 'error': response.json()})
        else:
            print("Form is invalid:", form.errors)  # Debug: Print form errors
    else:
        form = CreateUserForm()
    return render(request, 'userCreate.html', {'form': form})
#============= Deposit money to bank account ================== 
def deposit_money_view(request):
    if request.method == 'POST':
        form = DepositMoneyForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            for key, value in cleaned_data.items():
                if isinstance(value, Decimal):
                    cleaned_data[key] = str(value) 
            response = requests.post(f'{API_URL}/users/deposit', data=json.dumps(cleaned_data),
                headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                return redirect('success')
            else:
                return render(request, 'depositMony.html', {'form': form, 'error': response.json()})
    else:
        form = DepositMoneyForm()
    return render(request, 'depositMony.html', {'form': form})
#========== withdraw money from account ================
def withdraw_money_view(request):
    if request.method == 'POST':
        form = DepositMoneyForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            for key, value in cleaned_data.items():
                if isinstance(value, Decimal):
                    cleaned_data[key] = str(value) 
            response = requests.post(f'{API_URL}/users/withdraw', data=json.dumps(cleaned_data),
                headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                return redirect('success')
            else:
                return render(request, 'withdraw.html', {'form': form, 'error': response.json()})
    else:
        form = DepositMoneyForm()
    return render(request, 'withdraw.html', {'form': form})

def onlineTransaction(request):
    if request.method == 'POST':
        form = TransferFundsForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            for key, value in cleaned_data.items():
                if isinstance(value, Decimal):
                    cleaned_data[key] = str(value) 
            response = requests.post(f'{API_URL}/users/transfer_funds', data=json.dumps(cleaned_data),
                headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                return redirect('success')
            else:
                return render(request, 'transferFunds.html', {'form': form, 'error': response.json()})
    else:
        form = TransferFundsForm()
    return render(request, 'transferFunds.html', {'form': form})

def success_view(request):
    return render(request, 'success.html')
