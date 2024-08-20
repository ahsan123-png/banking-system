from django import forms

class CreateUserForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    father_name = forms.CharField(label='Father Name', max_length=100)
    mother_name = forms.CharField(label='Mother Name', max_length=100)
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.SelectDateWidget)
    profession = forms.CharField(label='Profession', max_length=100)
    account_type = forms.CharField(label='Account Type', max_length=100)
    cnic = forms.CharField(label='CNIC', max_length=15)
    phone_number = forms.CharField(label='Phone Number', max_length=15)
    email = forms.EmailField(label='Email')
    gender = forms.CharField(label='Gender', max_length=10)
    bank_name = forms.CharField(label='Bank Name', max_length=100, initial='Default Bank')

class DepositMoneyForm(forms.Form):
    acc_no = forms.CharField(label='Account Number', max_length=100)
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)

class TransferFundsForm(forms.Form):
    sender_account_number = forms.CharField(label='Sender Account Number', max_length=100)
    receiver_account_number = forms.CharField(label='Receiver Account Number', max_length=100)
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)
