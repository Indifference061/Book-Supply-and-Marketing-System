# -*- coding = utf-8 -*-
# @Auther : Zoe
# @File : testUrllib .py
# @Software : PyCharm

from django.urls import path
from . import views

app_name='System'

urlpatterns = [
    path('', views.home, name='home'),
    path('base',views.base,name='base'),
    path('bookshop', views.BookShopView.as_view(), name='bookshop'),
    path('bookstock', views.BookstockView.as_view(), name='bookstock'),
    path('info_detail/<int:book_id>/', views.InfoDetailView.as_view(), name='info_detail'),
    path('stockbills', views.StockBillsView.as_view(), name='stockbills'),
    path('stock', views.StockView.as_view(), name='stock'),
    path('new_book', views.NewBookView.as_view(), name='new_book'),
    path('finance', views.FinanceView.as_view(), name='finance'),

]
