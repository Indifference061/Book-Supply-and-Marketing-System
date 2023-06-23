from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from datetime import date


class UserManager(BaseUserManager):  # 为用户模型定义的自定义用户管理器，
    # 拓展了BaseUserManager，定义创建普通管理员用户和超级管理员用户
    def _create_user(self, username, password, uid, **kwargs):
        if not username:
            raise ValueError("请传入用户名！")
        if not password:
            raise ValueError("请传入密码！")
        user = self.model(username=username, uid=uid, **kwargs)
        user.set_password(password)  # 使用内置函数进行密码加密
        user.save()
        return user

    def create_user(self, username, password, uid, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(username, password, uid, **kwargs)

    def create_superuser(self, username, password, uid, **kwargs):
        kwargs['is_superuser'] = True
        return self._create_user(username, password, uid, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    # 建立User表单，
    # 继承django.contrib.auth.models中的内置AbstractBaseUser和PermissionsMixin
    # 拓展默认的User模型，password定义好了故不重复定义，
    # 对登录，注册，权限管理，哈希加密密码等操作直接用内置函数即可
    # 参考博客https://blog.csdn.net/zjy123078_zjy/article/details/104453236
    id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=11, unique=True, verbose_name="工号")
    username = models.CharField(max_length=18, verbose_name="用户名", unique=True)
    realname = models.CharField(max_length=20, verbose_name="真实姓名", null=True, blank=True)
    GENDER_TYPE = (
        ("1", "男"),
        ("2", "女")
    )
    gender = models.CharField(max_length=2, choices=GENDER_TYPE, verbose_name="性别", default=1, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号码")
    email = models.EmailField(verbose_name="邮箱",blank=True,null=True,unique=True)
    birthday = models.DateField(verbose_name="出生年月", default='2000-01-01')
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    is_staff = models.BooleanField(default=True, verbose_name="是否是管理员")
    is_superuser = models.BooleanField(default=False,verbose_name="是否是超级管理员用户")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [ 'uid',]

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    @property  # 令getgender作为类属性而不是类函数
    def getgender(self):
        return self.get_gender_display()  # choices独有的数据显示方法函数

    @property
    def getbirth(self):
        return str(self.birthday)

    @property
    def age(self):
        diff_days = date.today() - self.birthday
        class Meta:
            verbose_name = "年龄"
        return int(diff_days.days / 365)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
