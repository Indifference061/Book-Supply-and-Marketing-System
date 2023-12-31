# Generated by Django 4.0.4 on 2023-04-29 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='单价')),
                ('amount', models.IntegerField(verbose_name='数量')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='订单日期')),
            ],
        ),
        migrations.CreateModel(
            name='BookInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ISBN', models.CharField(max_length=20, unique=True, verbose_name='ISBN')),
                ('name', models.CharField(max_length=40, verbose_name='书名')),
                ('publisher', models.CharField(max_length=50, verbose_name='出版社')),
                ('author', models.CharField(max_length=50, verbose_name='作者')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='单价')),
                ('amount', models.IntegerField(default=0, verbose_name='数量')),
                ('is_active', models.BooleanField(default=False, verbose_name='是否上架')),
            ],
        ),
        migrations.CreateModel(
            name='SaleBill',
            fields=[
                ('bill_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='System.bill')),
                ('status', models.CharField(choices=[('1', '已付款')], default='1', max_length=2, verbose_name='状态')),
            ],
            bases=('System.bill',),
        ),
        migrations.CreateModel(
            name='StockBill',
            fields=[
                ('bill_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='System.bill')),
                ('status', models.CharField(choices=[('1', '未付款'), ('2', '已付款'), ('3', '已退货'), ('4', '已到货'), ('5', '已入库')], default='1', max_length=2, verbose_name='状态')),
            ],
            bases=('System.bill',),
        ),
        migrations.CreateModel(
            name='Finance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_stock', models.BooleanField(default=True, verbose_name='是否是进货订单')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='System.bill')),
            ],
        ),
        migrations.AddField(
            model_name='bill',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='System.bookinfo'),
        ),
    ]
