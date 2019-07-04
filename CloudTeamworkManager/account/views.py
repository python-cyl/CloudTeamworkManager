from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import logout as remove_session
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.forms import ValidationError
from .forms import RegisterForm, LoginForm, GetPasswordForm, change_info, extend_info
from .models import UserProfile
from .msgcode import sendcode
from task.models import task
from .forms import my_clean_phone_number
import json
import traceback


def logoutAccount(request):
    auth.logout(request)
    return HttpResponseRedirect("/account/login/")

def login_page(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect("/account/space/")
        forms = LoginForm()
        return render(request, 'login_page.html', {"form": forms})

    if request.method == "POST":
        forms = LoginForm(request.POST)

        if forms.is_valid():
            user = auth.authenticate(request, username = forms.cleaned_data['phone_number'], password = forms.cleaned_data['password'])
            if user:
                auth.login(request, user)
                return HttpResponseRedirect("/account/space/")
            return render(request, 'login_page.html', {"form": forms, "tip": "用户名或密码错误"})
        return render(request, 'login_page.html', {"form": forms, "tip": "输入内容有误"})

    if request.method == "DELETE":
         auth.logout(request)
         return HttpResponseRedirect("/account/login/")

def register_page(request):
    if request.method == "GET":
        forms = RegisterForm()
        return render(request, 'register_page.html', {"form": forms})

    if request.method == "POST":
        forms = RegisterForm(request.POST)
        forms.answer = request.session.get("verify")

        if forms.is_valid():
            user = User.objects.create_user(username = forms.cleaned_data['phone_number'], password=forms.cleaned_data['password'])
            UserProfile.objects.create(user_id = user.id)
            return HttpResponseRedirect("/account/login/")
        return render(request, 'register_page.html', {"form": forms})

def get_password_page(request):
    if request.method == "GET":
        forms = GetPasswordForm()
        return render(request, 'get_password_page.html', {"form": forms})

    if request.method == "POST":
        forms = GetPasswordForm(request.POST)
        forms.answer = request.session.get("verify")

        if forms.is_valid():
            user = User.objects.get(username = forms.cleaned_data["phone_number"])
            user.set_password(forms.cleaned_data["password"])
            user.save()
            return HttpResponseRedirect("/account/login/")
        return render(request, 'get_password_page.html', {"form": forms})

def check_phone_number(request):
    phone_number = request.POST.get("phone_number")

    try:
        my_clean_phone_number(phone_number)
    except ValidationError as e:
        return HttpResponse(e.message)
    return HttpResponse("手机号可用")

def sendmsgcode(request):
    def check_picode():
        answer = request.session.get('verify').upper()
        code = request.POST.get('picode').upper()

        if code == answer:
            remove_session(request)
            return True
        return False

    if check_picode():
        sendcode(request.POST.get("phone_number"))
        return HttpResponse("200")
    return HttpResponse('图形验证码校验失败')

@login_required
def space_page(request):
    user_info = UserProfile.objects.get(user_id = request.user.id)
    if user_info.name:
        return render(request, 'space.html')
    return HttpResponseRedirect("/account/perfect_information/")

@login_required
def personal_page(request):
    user_info = UserProfile.objects.get(user_id = request.user.id)
    involved_projects = json.loads(user_info["involved_projects"])
    projects_temp = []
    each_project_temp = {}
    for each_projects in involved_projects:
        task_id = each_projects
        task_status = task.objects.get(id = each_projects)["task_status"]
        each_project_temp["task_id"] = task_id
        each_project_temp["task_status"] = task_status
        projects_temp.append(each_project_temp)
    return render(request, "personal_page", {"user_info": user_info, "projects": projects_temp})

@login_required
def perfect_info(request):
    user_info = UserProfile.objects.get(user_id = request.user.id)
    if request.method == "GET":
        if user_info.name:
            return HttpResponseRedirect("/account/space/")
        form = extend_info()
        return render(request, 'perfect_information.html', {'form': form, "target_url": "/account/perfect_information/"})

    if request.method == "POST":
        user_info = UserProfile.objects.get(user_id = request.user.id)
        form = extend_info(request.POST, instance=user_info)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/account/space/")
        return render(request, 'perfect_information.html', {"form": form, "target_url": "/account/perfect_information/"})

# 处理用户修改个人信息的请求
# 要求用户登录，若没有登录，返回登录页面
@login_required
def change_info_page(request):

    # 从数据库中查找当前用户的个人信息
    user_info = UserProfile.objects.get(user_id = request.user.id)

    # 如果是get请求，则是打开页面的请求
    if request.method == "GET":

        # 将该用户的信息作为实例传入change_info表单的实例化函数，将会返回一个change_info表单的实例。
        # 这个实例中的字段将使用user_info中的信息填充
        form = change_info(instance=user_info)

        return render(request, 'perfect_information.html', {'form': form, "target_url": "/account/change_information/"})

    # 如果是post请求，则该请求希望修改一个用户的信息
    if request.method == "POST":

        # 将该用户的信息作为实例传入change_info表单的实例化函数，同时传入请求的post表单，将会返回一个change_info表单的实例。
        # 这个实例中的字段将先使用user_info中的信息填充，再使用post表单的信息填充。
        # 把user_info作为实例传入表单，一方面，可以指定需要修改的信息是user_info这个用户的信息
        # 另一方面，可以填充post表单中被隐藏的字段，例如name
        # 这样，用户的新信息完美覆盖到了旧信息上
        form = change_info(request.POST, instance=user_info)

        # 验证表单合法性
        if form.is_valid():
            form.save()
            return HttpResponse("200")
        return render(request, 'perfect_information.html', {"form": form, "target_url": "/account/change_information/"})
