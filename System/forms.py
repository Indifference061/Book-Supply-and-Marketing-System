from .models import *
from django import forms
from django.forms import fields
from django.forms import Form


class BookInfoForm(forms.ModelForm):
    class Meta:
        model = BookInfo
        fields = ['ISBN', 'name', 'author', 'publisher', 'price', 'amount', 'is_active']


class StockForm(forms.ModelForm):
    class Meta:
        model = StockBill
        fields = ['book', 'price', 'amount']


class SaleForm(forms.ModelForm):
    class Meta:
        model = SaleBill
        fields = ['amount']


class StockStatusForm(Form):
    paid = fields.BooleanField()
    back = fields.BooleanField()
    arrival = fields.BooleanField()



