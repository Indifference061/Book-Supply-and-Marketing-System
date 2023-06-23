from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(BookInfo)
admin.site.register(Bill)
admin.site.register(StockBill)
admin.site.register(SaleBill)
admin.site.register(Finance)
