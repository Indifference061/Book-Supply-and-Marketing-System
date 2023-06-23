from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate
from .forms import *
from .forms import RegisterForm, LoginForm
from django.views.generic import View
from System.models import *
from django.http import Http404

User = get_user_model()  # 获取User模型


def logout(request):
    request.session.clear()  # 清空session信息，退出登录
    return render(request, 'Userinfo/logout.html')


def register(request):
    if not request.user.is_superuser:  # 权限判断，只有超级管理员才能创建用户
        raise Http404
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():  # 利用form表单来对html传入的数据的合法性进行判断
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            last_user = User.objects.order_by('-uid').first()
            uid = str(int(last_user.uid)+1)
            username_ex = User.objects.filter(username=username).exists()
            if username_ex:
                context = {'form': LoginForm(), 'error': '用户名已存在'}
                return render(request,'Userinfo/register.html',context)

            User.objects.create_user(username=username,password=password,uid=uid)
            request.session["username"] = username  # 自定义session，login函数添加的session不满足时可以增加自定义的session信息。
            return render(request,'Userinfo/register.html',{'form': LoginForm(), 'msg': '创建成功'})
        else:
            return render(request,'Userinfo/register.html',{'form': LoginForm(), 'error': '无效输入，请保持密码一致'})
    else:
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'Userinfo/register.html', context)


def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            # 使用authenticate进行登录验证，验证成功会返回一个user对象，失败则返回None
            # 使用authenticate验证时如果is_active为False也会返回None，导致无法判断激活状态，
            # 此时可以在seetings中配置：
            # AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']
            if user:
                login(request, user)  # 使用自带的login函数进行登录，会自动添加session信息
                request.session["username"] = username  # 自定义session，login函数添加的session不满足时可以增加自定义的session信息。
                return redirect('System:home')
            else:
                context = {'form': LoginForm(), 'error': '用户名不存在或用户名与密码不匹配，请重新输入'}
                return render(request, 'Userinfo/login.html', context)
        else:
            context = {'form': LoginForm(), 'error': '输入无效！','form.errors':form.errors}
            return render(request, 'Userinfo/login.html', context)
    else:
        context = {'form': LoginForm()}
        return render(request, 'Userinfo/login.html', context)


class UserInfo(View):  # 返回一个可调用的视图，该视图接收请求并返回响应，
    # 当视图是请求/响应循环期间调用时， HttpRequest被分配到视图的request 属性。
    redirect_authenticated_user = True

    def get(self, request, user_id):  # 显示UserInfo
        user = User.objects.get(id=user_id)
        if(request.user != user):
            raise Http404
        form = UserChangeForm(instance=user)
        user_list = User.objects.order_by('uid')
        bill_list = SaleBill.objects.filter(user = user).order_by("-id")
        context = {'form': form, 'user': user, 'bill_list': bill_list, 'user_list': user_list}
        return render(request, 'Userinfo/userinfo.html' ,context)

    def post(self, request, user_id):  # 得到Userinfo的修改信息并显示，user_id为url的参数，传入进行对比
        user = User.objects.get(id=user_id)
        form = UserChangeForm(instance=user,data=request.POST,files=request.FILES)  # 直接调用UserChangeForm利用表单修改属性值
        bill_list = SaleBill.objects.filter(user = user).order_by("-id")
        user_list = User.objects.order_by('uid')

        if form.is_valid():
            form.save()  # 修改并保存进数据库
            context = {'form': form, 'user': user, 'bill_list': bill_list, 'user_list': user_list}
            return render(request,  'Userinfo/userinfo.html',context)
        else:
            errors = {name:list(form.errors[name]) for name in form.errors}
            context = {'form': form, 'error_msg': 'Invalid input', 'errors': errors, 'bill_list': bill_list, 'user_list': user_list}
            return render(request,  'Userinfo/userinfo.html',context)


