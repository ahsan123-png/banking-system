from decimal import Decimal
import json
import random
from typing import Any
from django.http import JsonResponse
from userRegistration.models import Account, Transaction,Bank
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializer import *
#=========  API Create =============
#create user 
@csrf_exempt
def createUser(request):
    if request.method == 'POST':
        try:
            data = get_request_body(request)
            name = data.get('name', '')
            father_name = data.get('father_name', '')
            mother_name = data.get('mother_name', '')
            date_of_birth = data.get('date_of_birth', '')
            profession= data.get('profession', '')
            account_type = data.get('account_type', '')
            cnic = data.get('cnic', '')
            phone_number = data.get('phoneNumber', '')
            email = data.get('email', '')
            gender = data.get('gender')
            bank_name = data.get('bank_name','Default Bank')
            # username = email.split("@")[0]
            user = UserEx.objects.create(
                name=name,
                father_name=father_name,
                mother_name=mother_name,
                gender=gender,
                date_of_birth=date_of_birth,
                phone_number=phone_number,
                profession=profession,
                email=email,
                accountType=account_type,
                cnic=cnic,
                bank_name=bank_name
            )
            user.save()
            return JsonResponse(good_response
                                (request.method,
                                {"success": "Data added successfully"},status=201))
        except Exception as e:
            return JsonResponse(bad_response
                                (request.method, str(e),
                                  status=400))
    else:
        return JsonResponse(bad_response(request.method, 
                                         f"{request.method} not allowed", 
                                         status=405))
#=========== deposit cash into account ======
@csrf_exempt
def depositMoney(request):
    if request.method == 'POST':
        data = get_request_body(request)
        account_number = data.get('acc_no')
        amount = Decimal(data.get('amount'))
        try:
            account = Account.objects.get(acc_no=account_number)
            account.balance += amount
            account.save()
            Transaction.objects.create(
                # when cash is deposit to account the sender is self and receiver is also self 
                receiver=account,
                sender=account,
                amount=amount,
                transaction_type='deposit',
                description=f'{amount} deposit to account {account.acc_no}'
            )
            return JsonResponse(
                good_response(
                    request.method,
                    {'success': 'Cash has been deposited successfully'},
                    status=200
                )
            )
        except Account.DoesNotExist:
            return JsonResponse(
                bad_response(
                    request.method,
                    'Account not found',
                    status=404
                )
            )
    else:
        return JsonResponse(
            bad_response(
                request.method,
                f'{request.method} not allowed',
                status=405
            )
        )
# ====== Cash withdraw ===========
@csrf_exempt
def withdrawCash(request):
    if request.method == 'POST':
        data = get_request_body(request)
        account_number = data.get('acc_no')
        amount = Decimal(data.get('amount'))
        try:
            account = Account.objects.get(acc_no=account_number)
            account.balance -= amount
            account.save()
            Transaction.objects.create(
                # when cash is deposit to account the sender is self and receiver is also self 
                receiver=account,
                sender=account,
                amount=amount,
                transaction_type='withdrawal',
                description=f'{amount} withdraw from account {account.acc_no}'
            )
            return JsonResponse(
                good_response(
                    request.method,
                    {'success': 'Cash has been Withdraw successfully'},
                    status=200
                )
            )
        except Account.DoesNotExist:
            return JsonResponse(
                bad_response(
                    request.method,
                    'Account not found',
                    status=404
                )
            )
    else:
        return JsonResponse(
            bad_response(
                request.method,
                f'{request.method} not allowed',
                status=405
            )
        )
# ====== transactions ============
@csrf_exempt
def transferFunds(request):
    if request.method == 'POST':
        data = get_request_body(request)
        sender_account_number = data.get('sender_account_number')
        receiver_account_number = data.get('receiver_account_number')
        amount = Decimal(data.get('amount'))
        try:
            sender = Account.objects.select_related('user', 'user__bank').get(acc_no=sender_account_number)
            receiver = Account.objects.select_related('user', 'user__bank').get(acc_no=receiver_account_number)
        except Account.DoesNotExist:
            return JsonResponse(bad_response(
                request.method,
                {'error': 'Account not found'},
                status=404
            ))
        if sender.balance >= amount:
            # Calculate the fee
            fee = Decimal('0.00')
            if sender.user.bank_name != receiver.user.bank_name:
                #10*amount/100 ---> percentage
                fee = amount * Decimal('0.3')  # 10% fee for interbank transfer
            transaction = Transaction.objects.create(
                sender=sender,
                receiver=receiver,
                amount=amount,
                fee=fee,
                transaction_type='transfer'
            )
            sender.balance -= amount + fee
            receiver.balance += amount
            sender.save()
            receiver.save()
            return JsonResponse(good_response(
                request.method,
                {'success': 'Funds transferred successfully'},
                status=200
            ))
        else:
            return JsonResponse(bad_response(
                request.method,
                {'error': 'Insufficient balance'},
                status=400
            ))
    else:
        return JsonResponse(bad_response(
            request.method,
            f'{request.method} not allowed',
            status=405
        ))

# ========== transaction_history ===========
@csrf_exempt
def transactionHistory(request,user_id):
    if request.method == 'GET':
        user=UserEx.objects.get(id=user_id)
        account=Account.objects.filter(user=user)
        # user id to get all relevant transections 
        account_id=account.values_list('id' , flat=True)
        transaction=Transaction.objects.filter(sender_id__in=account_id) | Transaction.objects.filter(receiver_id__in=account_id) 
        serializer=TransactionSerializer(transaction,many=True).data
        return JsonResponse(
            good_response(
                request.method,
                {
                    'record' : serializer 
                }
            )
        )
    else:
        return JsonResponse(bad_response(
            request.method,
            f'{request.method} not allowed',
            status=405
        ))


#+++++++ some useful methods ++++++++++
def generate_username():
    username = ""
    capitalize = [True, False]
    for i in range(0, 31):
        if capitalize[random.randint(0, 1)]:
            username += chr(random.randint(97, 117))
        else:
            username += chr(random.randint(65, 91))
    return username

# Sub Methods


def get_request_body(request):
    return json.loads(request.body)


def good_response(method: str, data: dict | Any, status: int = 200):
    return {
        "success": True,
        "data": data,
        "method": method,
        "status": status,
    }


def bad_response(method: str, reason: str, status: int = 403, data: dict | Any = None):
    return {
        "success": False,
        "reason": reason,
        "data": data,
        "status": status,
        "method": method,
    }
