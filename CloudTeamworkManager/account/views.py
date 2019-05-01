from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm, LoginForm, GetPasswordForm, change_info, extend_info
from .models import UserProfile
from .msgcode import sendcode


def login_page(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect("/account/space/")
        forms = LoginForm()
        return render(request, 'login_page.html', {"form": forms})

    if request.method == "POST":
        forms = LoginForm(request.POST)

        if forms.is_valid():
            user = auth.authenticate(request, username = forms.cleaned_data['user_name'], password = forms.cleaned_data['password'])
            if user:
                auth.login(request, user)
                return render(request, 'login_page.html')
            return render(request, 'login_page.html', {"form": forms, "tip": "用户名或密码错误"})
        return render(request, 'login_page.html', {"form": forms, "tip": "输入内容有误"})

    if request.method == "DELETE":
         logout(request)
         return HttpResponseRedirect("/account/login/")

def register_page(request):
    if request.method == "GET":
        forms = RegisterForm()
        return render(request, 'register_page.html', {"form": forms})

    if request.method == "POST":
        forms = RegisterForm(request.POST)

        if forms.is_valid():
            User.objects.create_user(username = forms.cleaned_data['user_name'], password=forms.cleaned_data['password'])
            UserProfile.objects.create(user_id = user.id, phone_number = forms.cleaned_data['phone_number'])
            return HttpResponse("200")
        return render(request, 'register_page.html', {"form": forms})

def get_password_page(request):
    if request.method == "GET":
        forms = GetPasswordForm()
        return render(request, 'get_password_page.html', {"form": forms})

    if request.method == "POST":
        forms = GetPasswordForm(request.POST)
        if forms.is_valid():
            user = User.objects.get(username = forms.cleaned_data["user_name"])
            user.set_password(forms.cleaned_data["password"])
            user.save()
            return HttpResponse("200")
        return render(request, 'get_password_page.html', {"form": forms})

def check_username(request):
    forms = UsernameForm(request.POST)

    if forms.is_valid():
        return HttpResponse("用户名可用")
    return HttpResponse("用户名不可用")

def check_phone_number(request):
    forms = UsernameForm(request.POST)

    if forms.is_valid():
        return HttpResponse("手机号可用")
    return HttpResponse("手机号不可用")

def sendmsgcode(request):
    def check_piccode():
        answer = request.session.get('verify').upper()
        code = request.POST.get('picode').upper()

        if code == answer:
            remove_session(request)
            return 1
        return 0

    if check_piccode():
        return HttpResponse("200")
    return HttpResponse('图形验证码校验失败')

@login_required
def space_page(request):
    user_info = UserProfile.objects.get(user_id = request.user.id)
    if user_info.name:
        return render(request, 'space.html')
    else:
        return HttpResponseRedirect("/account/perfect_information/")

@login_required
def perfect_info(request):
    user_info = UserProfile.objects.get(user_id = request.user.id)
    if request.method == "GET":
        form = extend_info(instance = user_info)
        return render(request, 'perfect_information.html', {'form': form, "target_url": "/account/perfect_information/"})
    
    if request.method == "POST":
        form = extend_info(request.POST, instance=user_info)
        if form.is_valid():
            form.save()
            return HttpResponse("200")
        return render(request, 'perfect_information.html', {"form": form, "target_url": "/account/perfect_information/"})

@login_required
def change_info_page(request):
    user_info = UserProfile.objects.get(user_id = request.user.id)
    if request.method == "GET":
        form = change_info(instance=user_info)
        return render(request, 'perfect_information.html', {'form': form, "target_url": "/account/change_information/"})

    if request.method == "POST":
        form = change_info(request.POST, instance=user_info)
        if form.is_valid():
            form.save()
            return HttpResponse("200")
        return render(request, 'perfect_information.html', {"form": form, "target_url": "/account/change_information/"})

#def login_submit(request):
#    forms = LoginForm(request.POST)

#    if forms.is_valid():
#        user = auth.authenticate(request, username = forms.cleaned_data['user_name'], password = forms.cleaned_data['password'])
#        if user:
#            auth.login(request, user)
#            return render(request, 'login_page.html')
#        else:
#            return render(request, 'login_page.html', {"form": forms, "tip": "用户名或密码错误"})
#    else:
#        return render(request, 'login_page.html', {"form": forms, "tip": "输入内容有误"})

#def register_submit(request):
#    forms = RegisterForm(request.POST)

#    if forms.is_valid():
#        code = verifycode(forms.cleaned_data['phone_number'], forms.cleaned_data['msgcode'])
#        if code:
#            user = User.objects.get(username = forms.cleaned_data['user_name'])
#            phone_number = UserProfile.objects.get(phone_number = forms.cleaned_data['phone_number'])
#            if not user:
#                if not phone_number:
#                    User.objects.create_user(username = forms.cleaned_data['user_name'], password=forms.cleaned_data['password'])
#                    UserProfile.objects.create(user_id = user.id, phone_number = forms.cleaned_data['phone_number'])
#                    return HttpResponse("200")
#                else:
#                    return render(request, 'register_page.html', {"form": forms, "tip": "手机号已被注册"})
#            else:
#                return render(request, 'register_page.html', {"form": forms, "tip": "用户已存在"})
#        else:
#            return render(request, 'register_page.html', {"form": forms, "tip": "短信验证码有误"})
#    else:
#        return render(request, 'register_page.html', {"form": forms, "tip": "输入内容有误"})

#def get_password_submit(request):
#    forms = GetPasswordForm(request.POST)

#    if forms.is_valid():
#        code = verifycode(forms.cleaned_data['phone_number'], forms.cleaned_data['msgcode'])
#        if code:
#            user = User.objects.get(username = forms.cleaned_data["user_name"])
#            user.set_password(forms.cleaned_data["password"])
#            user.save()
#            return HttpResponse("200")
#        else:
#            return render(request, 'get_password.html', {"form": forms, "tip": "短信验证码有误"})
#    else:
#        return render(request, 'get_password.html', {"form": forms, "tip": "输入内容有误"})

#@login_required
#def extend_info_submit(request):
#    user_info = UserProfile.objects.get(user_id = request.user.id)
#    form = extend_info(request.POST, instance=user_info)
#    if form.is_valid():
#        form.save()
#        return HttpResponse("200")
#    else:
#        return render(request, 'perfect_information.html', {"form": form, "target_url": "/account/perfect_information/submit/"})

#@login_required
#def change_info_submit(request):
#    user_info = UserProfile.objects.get(user_id = request.user.id)
#    form = change_info(request.POST, instance=user_info)
#    if form.is_valid():
#        form.save()
#        return HttpResponse("200")
#    else:
#        return render(request, 'perfect_information.html', {"form": form, "target_url": "/account/change_information/submit/"})
