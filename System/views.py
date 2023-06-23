from django.views.generic import View
from .forms import *
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request, 'System/home.html')


def base(request):
    return render(request, 'System/base.html')


@method_decorator(login_required(login_url='/Userinfo/login'), name='dispatch')
class BookShopView(View):  # 书店页面视图，进行传输书目、购买的对应后端操作

    def get(self, request):  # 若请求是GET，搜索并展示对应书
        search_ISBN = request.GET.get('search_ISBN')
        search_name = request.GET.get('search_name')
        search_publisher = request.GET.get('search_publisher')
        search_author = request.GET.get('search_author')
        if search_ISBN is None:  # 增加判断修改语句，否则在数据库中筛选会报错
            search_ISBN = ''
        if search_name is None:
            search_name = ''
        if search_publisher is None:
            search_publisher = ''
        if search_author is None:
            search_author = ''
        books_list = list(BookInfo.objects.filter(amount__gt=0,price__gt=0,is_active=1,
                                                  ISBN__icontains=search_ISBN, name__icontains=search_name,
                                                  publisher__icontains=search_publisher, author__icontains=search_author).order_by('id'))
        context = {'books_list': books_list, 'ISBN': search_ISBN, 'name': search_name,
                   'author': search_author, 'publisher': search_publisher, }
        return render(request, 'System/bookshop.html', context)

    def post(self, request):  # 若是POST请求，进行购买
        search_ISBN = request.GET.get('search_ISBN')
        search_name = request.GET.get('search_name')
        search_publisher = request.GET.get('search_publisher')
        search_author = request.GET.get('search_author')
        if search_ISBN is None:  # 增加判断修改语句，否则在数据库中筛选会报错
            search_ISBN = ''
        if search_name is None:
            search_name = ''
        if search_publisher is None:
            search_publisher = ''
        if search_author is None:
            search_author = ''
        books_list = list(BookInfo.objects.filter(amount__gt=0, price__gt=0, is_active=1,
                                                  ISBN__icontains=search_ISBN, name__icontains=search_name,
                                                  publisher__icontains=search_publisher,author__icontains=search_author).order_by('id'))
        amount = request.POST.get('amount')
        ISBN = request.POST.get('ISBN')
        price = request.POST.get('price')
        user_id = request.POST.get('user_id')
        book = BookInfo.objects.get(ISBN=ISBN)
        if amount is None or amount == '':
            context={'books_list': books_list, 'error_msg': '请输入购买量!', 'wrong_ISBN': ISBN}
            return render(request, 'System/bookshop.html',context)
        if book.amount - int(amount) < 0:
            context={'books_list': books_list, 'error_msg': '库存不足，请重新输入购买量!','wrong_ISBN': ISBN}
            return render(request, 'System/bookshop.html',context)
        book.amount = book.amount - int(amount)
        book.save()
        user = User.objects.get(id=user_id)  # 获取User表中的对应user_id的用户 用于后面记录在bill的用户属性中
        salebill = SaleBill(book=book, user=user, price=price, amount=amount)  # 创建一条新的salebill 元组
        salebill.save()
        finance = Finance(bill=salebill, is_stock=0)  # 创建一个新的finance 元组
        finance.save()
        return redirect('System:bookshop')  # 重定向并再次发起请求刷新数据


@method_decorator(login_required(login_url='/Userinfo/login'), name='dispatch')  # 限制登录才能实现的功能
class BookstockView(View):  # 控制书库页面，对网页发出的上下架请求，设置零售价请求和搜索请求对后端数据库进行调用和修改

    def get(self, request):  # 网页发出GET请求进行展示搜索书目
        search_ISBN = request.GET.get('search_ISBN')
        search_name = request.GET.get('search_name')
        search_publisher = request.GET.get('search_publisher')
        search_author = request.GET.get('search_author')
        if search_ISBN is None:  # 增加判断修改语句，否则在数据库中筛选会报错
            search_ISBN = ''
        if search_name is None:
            search_name = ''
        if search_publisher is None:
            search_publisher = ''
        if search_author is None:
            search_author = ''
        books_list = list(BookInfo.objects.filter(ISBN__icontains=search_ISBN, name__icontains=search_name,
                            publisher__icontains=search_publisher, author__icontains=search_author).order_by('id'))
        context = {'books_list': books_list, 'ISBN': search_ISBN, 'name': search_name,
                   'author': search_author, 'publisher': search_publisher, }
        return render(request, 'System/bookstock.html',context)

    def post(self, request):  # 网页发出POST请求进行对应操作
        activate = request.POST.get('activate')  # 获取网页传来的上下架请求，并进行判断操作
        deactivate = request.POST.get('deactivate')
        price = request.POST.get('price')
        ISBN = request.POST.get('ISBN')
        book = BookInfo.objects.get(ISBN=ISBN)  # 根据网页操作的书籍的ISBN找到对应的书

        search_ISBN = request.GET.get('search_ISBN')
        search_name = request.GET.get('search_name')
        search_publisher = request.GET.get('search_publisher')
        search_author = request.GET.get('search_author')
        if search_ISBN is None:
            search_ISBN = ''
        if search_name is None:
            search_name = ''
        if search_publisher is None:
            search_publisher = ''
        if search_author is None:
            search_author = ''
        books_list = list(BookInfo.objects.filter(ISBN__icontains=search_ISBN, name__icontains=search_name,
                            publisher__icontains=search_publisher, author__icontains=search_author).order_by('id'))

        if activate:  # 进行上架操作
            if book.amount == 0:
                context = {'books_list': books_list, 'ISBN': search_ISBN, 'name': search_name,
                           'author': search_author, 'publisher': search_publisher, 'error_msg': '库存不够，请先进货！', 'wrong_ISBN': ISBN}
                return render(request, 'System/bookstock.html',context)
            book.price = price  # 更新书籍价格
            book.is_active = 1  # 更改书籍上架属性
            book.save()
            search_ISBN = request.GET.get('search_ISBN')
            search_name = request.GET.get('search_name')
            search_publisher = request.GET.get('search_publisher')
            search_author = request.GET.get('search_author')
            if search_ISBN is None:
                search_ISBN = ''
            if search_name is None:
                search_name = ''
            if search_publisher is None:
                search_publisher = ''
            if search_author is None:
                search_author = ''
            books_list = list(BookInfo.objects.filter(ISBN__icontains=search_ISBN, name__icontains=search_name,
                                                      publisher__icontains=search_publisher, author__icontains=search_author).order_by('id'))
            context = { 'books_list': books_list, 'ISBN': search_ISBN, 'name': search_name,
                       'author': search_author, 'publisher': search_publisher, }
            return render(request, 'System/bookstock.html', context)

        if deactivate:  # 进行下架操作
            book.is_active = 0  # 更改书籍上架属性
            book.save()
            search_ISBN = request.GET.get('search_ISBN')
            search_name = request.GET.get('search_name')
            search_publisher = request.GET.get('search_publisher')
            search_author = request.GET.get('search_author')
            if search_ISBN is None:
                search_ISBN = ''
            if search_name is None:
                search_name = ''
            if search_publisher is None:
                search_publisher = ''
            if search_author is None:
                search_author = ''
            books_list = list(BookInfo.objects.filter(ISBN__icontains=search_ISBN, name__icontains=search_name,
                                                      publisher__icontains=search_publisher,author__icontains=search_author).order_by('id'))
            context = {'books_list': books_list, 'ISBN': search_ISBN, 'name': search_name,
                       'author': search_author, 'publisher': search_publisher, }
            return render(request, 'System/bookstock.html', context)



@method_decorator(login_required(login_url='/Userinfo/login'), name='dispatch')
class StockView(View):  # 进货部分
    def get(self, request):  # get请求时对应的操作，获取书籍列表并在网页中显示

        search_id = request.GET.get('search_id')  # 获取网页传入的id
        books = BookInfo.objects.all()  # 得到数据库中所有书的列表
        if search_id is None or search_id == '':  # 若没有输入id，展示所有书
            form = StockForm()
            books_list = books.order_by("id")
            context = {'form': form, 'books_list': books_list}
            return render(request, 'System/stock.html',context)
        books_list = books.filter(id=search_id).order_by("id")  # 若输入了id则查询对应的书籍，此处不能使用get否则容易出现网页报错显示数据库中不存在
        book = books_list.first()
        form = StockForm(initial={'book': book})
        context={'form': form, 'books_list': books_list}
        return render(request, 'System/stock.html',context)

    def post(self, request):
        form = StockForm(data=request.POST)  # 直接获取表单
        user_id = form.data.get('user_id')  # 获取当前操作用户的id
        if form.is_valid():  # 若表单获取的数据信息有效
            book_id = form.data.get('book')  # 获取表单中的书、进价、数量的信息
            price = form.data.get('price')
            amount = form.data.get('amount')
            # print(user_id)
            user = User.objects.get(id=user_id)  # 从数据库中获取对应user、bookinfo信息
            book = BookInfo.objects.get(id=book_id)
            stockbill = StockBill(book=book, price=price, amount=amount, user=user)  # 创建新的stockbill元组
            stockbill.save()
            return redirect('System:stockbills')
        else:
            print("无效")
            context={'form': form, 'error_msg': '检查输入格式'}
            return render(request, 'System/stock.html',context)



@method_decorator(login_required(login_url='/Userinfo/login'), name='dispatch')
class StockBillsView(View):  # 记录书库中流水
    def get(self, request):

        form = StockStatusForm()
        bills_list = list(StockBill.objects.all().order_by('-id'))
        context={'form': form, 'bills_list': bills_list}
        return render(request, 'System/stockbills.html', context)

    def post(self, request):
        form = StockStatusForm(data=request.POST)  # 获取网页传输的进货的表单
        paid = form.data.get('paid')
        back = form.data.get('back')
        arrival = form.data.get('arrival')
        bill_id = form.data.get('bill_id')
        bill = StockBill.objects.get(id=bill_id)
        # print(bill.status)
        # print(paid)
        if bill.status == "1" and paid == "1":  # 根据进货订单的不同的状态以及
            # 动态更改参数的值对订单状态进行修改
            # print(paid)
            bill.status = "2"
            bill.save()
            finan = Finance(bill=bill, is_stock=1)  # 付款后在财务中添加账单流水信息
            finan.save()

        elif bill.status == "1" and back == "1":
            bill.status = "3"
            bill.save()

        elif bill.status == "2" and arrival == "1":
            bill.status = "4"
            bill.save()

        elif bill.status == "4":
            book = BookInfo.objects.get(id=bill.book.id)  # 获取进货书籍并在后面进行修改
            bill.status = "5"   # 如果已到货再次调用post方法，就是点击了入库按钮，将状态改为已入库
            book.amount = book.amount + bill.amount  # 入库后增加对应书籍的库存
            book.save()
            bill.save()
        return redirect('System:stockbills')

@method_decorator(login_required(login_url='/Userinfo/login/'), name='dispatch')
class InfoDetailView(View):

    def get(self, request, book_id):
        book_info = BookInfo.objects.filter(id=book_id).first()
        form = BookInfoForm(instance=book_info)
        context={'form': form, 'book_info': book_info,}
        return render(request, 'System/info_detail.html' ,context)

    def post(self, request, book_id):
        book_info = BookInfo.objects.filter(id=book_id).first()
        form = BookInfoForm(instance=book_info, data=request.POST)  # 直接实例化BookInfo中的元组，接受一个现有的模型实例作为关键字参数 instance，并通过save直接修改
        if form.is_valid():
            # print(form)
            form.save()  # 通过表单进行修改
            context={'form': form, 'book_info': book_info,'msg':"修改成功"}
            return render(request, 'System/info_detail.html', context)
        else:
            # print(form.errors)
            context={'form': form, 'book_info': book_info, 'error_msg': '检查输入格式！'}
            return render(request,  'System/info_detail.html',context)



@method_decorator(login_required(login_url='/Userinfo/login'), name='dispatch')
class NewBookView(View):
    def get(self, request):
        form = BookInfoForm()
        context={'form': form}
        return render(request, 'System/new_book.html',context)

    def post(self, request):
        form = BookInfoForm(data=request.POST)  # 创建一个由POST传入的新表单，通过save在表中创建新元组
        if form.is_valid():
            form.save()
            return redirect('System:stock')
        else:
            context={'form': form, 'error_msg': '检查输入格式'}
            return render(request, 'System/new_book.html', context)


@method_decorator(login_required(login_url='/Userinfo/login'), name='dispatch')
class FinanceView(View):

    def get(self, request):
        search_start = request.GET.get('search_start')  # 获取订单的起始时间和中止时间
        search_end = request.GET.get('search_end')
        if search_start is None or search_start == '':  # 设置默认值
            search_start = '2023-01-01'
        if search_end is None or search_end == '':
            search_end = '2023-12-31'
        print(search_end)
        finance_list = list(Finance.objects.filter(date__gte=search_start, date__lte=search_end).order_by('-date'))  # 在数据库中进行筛选
        profit = 0  # 用于计算总利润、总收入、总支出
        outcome = 0
        income = 0
        for finance in finance_list:  # 进行计算
            temp = finance.income_int
            if temp > 0:
                income = income + temp
            elif temp < 0:
                outcome = outcome + temp
            profit = profit + temp
        print(profit)
        context={'finance_list': finance_list, 'search_start': search_start, 'search_end': search_end, 'profit': profit, 'income': income,
                               'outcome': outcome}
        return render(request, 'System/finance.html',context)




