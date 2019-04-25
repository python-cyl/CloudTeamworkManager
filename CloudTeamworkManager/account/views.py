from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm, LoginForm, extend_info, GetPasswordForm, change_info
from .models import UserProfile
from .msgcode import sendcode, verifycode


def login_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/account/space/")
    return render(request, 'login_page.html')

def register_page(request):
    return render(request, 'register_page.html')

def get_password_page(request):
    return render(request, 'get_password_page.html')

def login_submit(request):
    forms = LoginForm(request.POST)

    if forms.is_valid():
        user = auth.authenticate(request, username = forms.cleaned_data['user_name'], password = forms.cleaned_data['password'])
        if user:
            auth.login(request, user)
            return render(request, 'space.html')
        else:
            return HttpResponse("用户名或密码错误")
    else:
        return HttpResponse("输入内容有误")

def check_username(request):
    forms = UsernameForm(request.POST)

    if forms.is_valid():
        user = User.objects.get(username = forms.cleaned_data['user_name'])
        if user:
            return HttpResponse("用户名可用")
        else:
            return HttpResponse("用户名已被使用")
    else:
        return HttpResponse("输入内容有误")

def register_submit(request):
    forms = RegisterForm(request.POST)

    if forms.is_valid():
        code = verifycode(forms.cleaned_data['phone_number'], forms.cleaned_data['msgcode'])
        if code:
            user = User.objects.get(username = forms.cleaned_data['user_name'])
            if not user:
                User.objects.create_user(username = forms.cleaned_data['user_name'], password=forms.cleaned_data['password'])
                UserProfile.objects.create(user_id = user.id, phone_number = forms.cleaned_data['phone_number'])
                return HttpResponse("200")
            else:
                return HttpResponse("用户已存在")
        else:
            return HttpResponse("短信验证码错误")
    else:
        return HttpResponse("输入内容有误")

def get_password_submit(request):
    forms = GetPasswordForm(request.POST)

    if forms.is_valid():
        code = verifycode(forms.cleaned_data['phone_number'], forms.cleaned_data['msgcode'])
        if code:
            user = User.objects.get(username = forms.cleaned_data["user_name"])
            user.set_password(forms.cleaned_data["password"])
            user.save()
            return HttpResponse("200")
        else:
            return HttpResponse("短信验证码错误")
    else:
        return HttpResponse("输入内容有误")

def sendmsgcode(request):
    # 发送短信验证码
    def check_piccode():
        # 校验图形验证码
        answer = request.session.get('verify').upper()
        code = request.POST.get('picode').upper()
        # 把验证码答案和用户输入的内容都转为大写

        if code == answer:
            remove_session(request)
            return 1
        else:
            return 0

    if check_piccode():
        # 验证图形验证码
        phone_number = request.POST.get("phone_number")
        # 读取手机号
        phone_number = UserProfile.objects.get(phone_number = forms.cleaned_data['phone_number'])
        if phone_number:
            return HttpResponse("手机号已注册")
        else:
            result = sendcode(phone_number)
            # 发送验证码
            return HttpResponse(result)
            # 发送回执
    else:
        # 验证码校验失败
        return HttpResponse('412')

@login_required
def space_page(request):
    user_info = UserProfile.objects.get(user_id = request.user.id)
    if user_info.name:
        return render(request, 'space.html')
    else:
        form = extend_info(instance = user_info)
        return render(request, 'perfect_infomation.html', {'form': form})

@login_required
def extend_info_submit(request):
    user_info = UserProfile.objects.get(UserProfile, user_id = request.user.id)
    form = extend_info(request.POST, instance=user_info)
    if form.is_valid():
        form.save()
        return HttpResponse("200")
    else:
        return HttpResponse("输入内容有误")

@login_required
def change_info_submit(request):
    user_info = UserProfile.objects.get(user_id = request.user.id)
    form = change_info(request.POST, instance=user_info)
    if form.is_valid():
        form.save()
        return HttpResponse("200")
    else:
        return HttpResponse("输入内容有误")

@login_required
def change_info_page(request):
    user_info = UserProfile.objects.get(user_id = request.user.id)
    form = change_info(request.POST, instance=user_info)
    return render(request, 'perfect_infomation.html', {'form': form})
