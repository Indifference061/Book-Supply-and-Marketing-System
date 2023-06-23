from Userinfo.models import *


# Create your models here.

class BookInfo(models.Model):
    id = models.AutoField(primary_key=True)
    ISBN = models.CharField(max_length=20, null=False, unique=True,verbose_name="ISBN")
    name = models.CharField(max_length=40, null=False,verbose_name="书名")
    publisher = models.CharField(max_length=50, null=False,verbose_name="出版社")
    author = models.CharField(max_length=50, null=False,verbose_name="作者")
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True,verbose_name="单价")
    amount = models.IntegerField(default=0,verbose_name="数量")
    is_active = models.BooleanField(default=False,verbose_name="是否上架")

    def __str__(self):
        return self.name


class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE,verbose_name="书名")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False,verbose_name="单价")
    amount = models.IntegerField(null=False,verbose_name="数量")
    date = models.DateTimeField(auto_now_add=True,verbose_name="订单日期")

    @property
    def total_price(self):
        return self.price * self.amount

    def __str__(self):
        return self.id


class StockBill(Bill):
    STATUS_TYPE = (
        ("1", "未付款"),
        ("2", "已付款"),
        ("3", "已退货"),
        ("4", "已到货"),
        ("5", "已入库"),
    )
    status = models.CharField(max_length=2, choices=STATUS_TYPE, verbose_name="状态", default="1")

    @property
    def getstatus(self):
        return self.get_status_display()


class SaleBill(Bill):
    STATUS_TYPE = (
        ("1", "已付款"),
    )
    status = models.CharField(max_length=2, choices=STATUS_TYPE, verbose_name="状态", default="1")

    @property
    def getstatus(self):
        return self.get_status_display()


class Finance(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    is_stock = models.BooleanField(default=True,verbose_name="是否是进货订单")
    date = models.DateTimeField(auto_now_add=True)

    @property
    def type(self):
        if self.is_stock:
            return "进货"
        else:
            return "出售"

    @property
    def user(self):
        return self.bill.user

    @property
    def income_display(self):
        if self.is_stock:
            return "-"+str(self.bill.total_price)
        else:
            return "+" + str(self.bill.total_price)

    @property
    def income_int(self):
        if self.is_stock:
            return -(self.bill.total_price)
        else:
            return self.bill.total_price

    # @property
    # def getdate(self):
    #     return self.date.date()


