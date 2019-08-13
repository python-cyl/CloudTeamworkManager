from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.forms import ValidationError
from django.forms.models import model_to_dict
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm, LoginForm, GetPasswordForm, change_info, extend_info, ResetPasswordForm, my_clean_phone_number
from .models import UserProfile
from .msgcode import sendcode
from task.models import task
import json


def logoutAccount(request):
    auth.logout(request)
    return HttpResponseRedirect("/account/login/")

def login_page(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect("/account/space/")
        return render(request, 'login_page.html')

    if request.method == "POST":
        forms = LoginForm(request.POST)

        if forms.is_valid():
            user = auth.authenticate(request, username = forms.cleaned_data['phone_number'], password = forms.cleaned_data['password'])
            if user:
                auth.login(request, user)
                return HttpResponseRedirect("/account/space/")
            return JsonResponse({"tip": "用户名或密码错误", "status": 400}, safe=False)
        return JsonResponse({"tip": "输入内容有误", "status": 400}, safe=False)

    if request.method == "DELETE":
         auth.logout(request)
         return HttpResponseRedirect("/account/login/")

def register_page(request):
    if request.method == "GET":
        return render(request, 'register_page.html')

    if request.method == "POST":
        forms = RegisterForm(request.POST)
        forms.answer = request.session.get("verify")

        if forms.is_valid():
            user = User.objects.create_user(username = forms.cleaned_data['phone_number'], password=forms.cleaned_data['password'])
            UserProfile.objects.create(user_id = user.id)
            return HttpResponseRedirect("/account/login/")
        return JsonResponse({"tip": list(forms.errors.values())[0][0], "status": 400}, safe=False)

def get_password_page(request):
    if request.method == "GET":
        return render(request, 'get_password_page.html')

    if request.method == "POST":
        forms = GetPasswordForm(request.POST)

        if forms.is_valid():
            user = User.objects.get(username = forms.cleaned_data["phone_number"])
            user.set_password(forms.cleaned_data["password"])
            user.save()
            return HttpResponseRedirect("/account/login/")
        return JsonResponse({"tip": list(forms.errors.values())[0][0], "status": 400}, safe=False)

def reset_password(request):
    if request.method == "GET":
        return render(request, 'reset_password_page.html')

    if request.method == "POST":
        forms = ResetPasswordForm()
        user = request.user
        forms.user = user

        if forms.is_valid():
            user.set_password(forms.cleaned_data["new_password"])
            return HttpResponseRedirect("/account/login/")
        return JsonResponse({"tip": list(forms.errors.values())[0][0], "status": 400}, safe=False)

def check_phone_number(request):
    phone_number = request.POST.get("phone_number")

    try:
        my_clean_phone_number(phone_number)
    except ValidationError as e:
        return JsonResponse({"tip": e.message, "status": 400}, safe=False)
    return JsonResponse({"tip": "手机号码可用", "status": 200}, safe=False)

def sendmsgcode(request):
    def check_picode():
        answer = request.session.get('verify').upper()
        code = request.POST.get('picode').upper()

        if code == answer:
            auth.logout(request)
            return True
        return False

    if check_picode():
        sendcode(request.POST.get("phone_number"))
        return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
    return JsonResponse({"tip": "图形验证码校验失败", "status": 400}, safe=False)

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
    forms = extend_info(request.POST, instance=user_info)

    if forms.is_valid():
        forms.save()
        return HttpResponseRedirect("/account/space/")
    return JsonResponse({"tip": list(forms.errors.values())[0][0], "status": 400}, safe=False)

@login_required
def change_info(request):
    user_info = UserProfile.objects.get(user_id = request.user.id)
    forms = change_info(request.POST, instance=user_info)

    if forms.is_valid():
        forms.save()
        return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
    return JsonResponse({"tip": list(forms.errors.values())[0][0], "status": 400}, safe=False)
