from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, extend_info
from .models import UserProfile
from .msgcode import sendcode, verifycode


def login_page(request):
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
    pass

def data_is_valid(data_class, data_instance):
    attribute = list(data_class.base_fields)
    check_list = {each_attr: [getattr(data_class.base_fields[each_attr],"max_length", 9999), getattr(data_class.base_fields[each_attr],"min_length", -1)] for each_attr in attribute}
    for (each_key, each_value) in check_list.items():
        try:
            if each_value[0] <= len(getattr(data_instance, each_key, None)) < each_value[0]:
                continue
            break
        except:
            continue
    else:
        return True
    return False

@login_required
def space_page(request):
    user_info = get_object_or_404(UserProfile, user_id = request.user.id)
    form = extend_info(instance = user_info)
    if form.is_valid():
        return render(request, 'space.html')
    else:
        return render(request, 'perfect_infomation.html', {'form': form})

@login_required
def extend_info_submit(request):
    form = extend_info(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse("200")
    else:
        return HttpResponse("403")