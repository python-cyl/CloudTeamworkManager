from django.shortcuts import render, HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
from .models import UserProfile
from .msgcode import sendcode, verifycode


def login_page(request):
    return render(request, 'login_page.html')

def register_page(request):
    return render(request, 'register_page.html')

def getpassword_page(request):
    return render(request, 'getpassword_page.html')

def login_submit(request):
    forms = LoginForm(request.POST)

    if forms.is_valid():
        user = auth.authenticate(request, username = forms.cleaned_data['user_name'], password = forms.cleaned_data['password'])
        if user:
            auth.login(request, user)
            return render(request, 'space.html')
        else:
            return HttpResponse(401.1)
    else:
        return HttpResponse(401.7)

def register_submit(request):
    forms = RegisterForm(request.POST)

    if forms.is_valid():
        code = verifycode(forms.cleaned_data['phone_number'], forms.cleaned_data['msgcode'])
        if code:
            user = User.objects.create_user(forms.cleaned_data['user_name'], password = forms.cleaned_data['password'])
            user_info = UserProfile.objects.create(user_id = user.id, phone_number = forms.cleaned_data['phone_number'])
            return HttpResponse("200")
        else:
            return HttpResponse("417")
    else:
        return HttpResponse("403")

def get_password(request):
    phone_number = request.POST.get("phone_number")

