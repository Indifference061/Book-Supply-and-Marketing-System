from django.forms import Form,fields
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *
# 提供表单的一些后台相关的数据属性和错误信息

class LoginForm(Form):
    username = fields.CharField(required=True,min_length=1,max_length=20,error_messages={
            "required":"用户名不可以为空！",
            "min_length":"用户名不能低于1位！",
            "max_length":"用户名不能超过20位！"
        }
    )
    password = fields.CharField(required=True,widget=forms.PasswordInput,error_messages={
            "required":"密码不得为空",
        }
    )

class RegisterForm(Form):
    username = fields.CharField(required=True,min_length=1,max_length=20,error_messages={
            "required":"用户名不得为空！",
            "min_length":"用户名不得少于1位！",
            "max_length":"用户名不得多于20位！"
        }
    )
    password1 = fields.CharField(required=True,min_length=5,max_length=20,error_messages={
            "required":"密码不得空！",
            "min_length": "密码不得少于5位！",
            "max_length": "密码不得多于20位！"
        }
    )
    password2 = fields.CharField(required=True)

    def clean_password2(self):
        if not self.errors.get("password1"):
            if self.cleaned_data["password2"] != self.cleaned_data["password1"]:
                raise ValidationError("您输入的密码不一致，请重新输入！")
            return self.cleaned_data

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('uid', 'realname', 'gender','phone', 'email', 'birthday')
