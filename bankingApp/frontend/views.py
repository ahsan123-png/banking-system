from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .form import CreateUserForm, DepositMoneyForm, TransferFundsForm
import requests
from django.conf import settings


# def register(request):
#     return render(request,'userCreate.html')

API_URL = 'http://localhost:8000/api'

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            response = requests.post(f'{API_URL}/create', data=form.cleaned_data)
            if response.status_code == 201:
                return redirect('success')
            else:
                return render(request, 'userCreate.html', {'form': form, 'error': response.json()})
    else:
        form = CreateUserForm()
    return render(request, 'userCreate.html', {'form': form})

def deposit_money_view(request):
    if request.method == 'POST':
        form = DepositMoneyForm(request.POST)
        if form.is_valid():
            response = requests.post(f'{API_URL}/deposit', data=form.cleaned_data)
            if response.status_code == 200:
                return redirect('success')
            else:
                return render(request, 'frontend/deposit_money.html', {'form': form, 'error': response.json()})
    else:
        form = DepositMoneyForm()
    return render(request, 'frontend/deposit_money.html', {'form': form})

def transfer_funds_view(request):
    if request.method == 'POST':
        form = TransferFundsForm(request.POST)
        if form.is_valid():
            response = requests.post(f'{API_URL}/transfer_funds', data=form.cleaned_data)
            if response.status_code == 200:
                return redirect('success')
            else:
                return render(request, 'frontend/transfer_funds.html', {'form': form, 'error': response.json()})
    else:
        form = TransferFundsForm()
    return render(request, 'frontend/transfer_funds.html', {'form': form})

def success_view(request):
    return render(request, 'frontend/success.html')
