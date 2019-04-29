import re
from django.forms import ModelForm, ValidationError
from django import forms
from .models import UserProfile


class RegisterForm(forms.Form):
    user_name = forms.CharField(max_length=20, min_length=6)
    password = forms.CharField(max_length=16, min_length=6)
    msgcode = forms.CharField(max_length=4, min_length=4)
    phone_number = forms.CharField(max_length=11, min_length=11)

class UsernameForm(forms.Form):
    user_name = forms.CharField(max_length=20, min_length=6)

class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=11, min_length=11)

class LoginForm(forms.Form):
    password = forms.CharField(max_length=16, min_length=6)
    user_name = forms.CharField(max_length=20, min_length=6)

class GetPasswordForm(forms.Form):
    user_name = forms.CharField(max_length=20, min_length=6)
    password = forms.CharField(max_length=16, min_length=6)
    msgcode = forms.CharField(max_length=4, min_length=4)
    phone_number = forms.CharField(max_length=11, min_length=11)

class extend_info(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("management_projects", "unread_notifications", "read_notifications", "involved_projects", "user")
        
    def __init__(self, *args, **kwargs):
        super(extend_info, self).__init__(*args, **kwargs)
        self.fields["home_address"].required = False
        self.fields["guardian_phone"].required = False
        self.fields["introduction"].required = False

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")

        if re.match("^1[34578]\d{9}$", phone_number):
            return phone_number
        else:
            raise ValidationError("手机号码不正确")

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if re.match("^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$", email):
            return email
        else:
            raise ValidationError("电子邮箱不正确")

    def clean_room(self):
        room = self.cleaned_data.get("room")

        if re.match("\d{4,8}", room):
            return room
        else:
            raise ValidationError("宿舍号不正确")

    def clean_name(self):
        name = self.cleaned_data.get("name")

        if re.match("^([a-zA-Z0-9\u4e00-\u9fa5\·]{2,5})$", name):
            return name
        else:
            raise ValidationError("姓名不正确")

    def clean_student_id(self):
        student_id = self.cleaned_data.get("student_id")

        if re.match("\d{10}", student_id):
            return student_id
        else:
            raise ValidationError("学号不正确")

    def clean_grade(self):
        grade = self.cleaned_data.get("grade")

        if re.match("\d{4}", grade):
            return grade
        else:
            raise ValidationError("年级不正确")

class change_info(extend_info):
    class Meta:
        model = UserProfile
        exclude = ("name", "student_id", "cloud_id", "magor", "grade", "sex", "management_projects", "unread_notifications", "read_notifications", "involved_projects", "user")

    def clean_name(self):
        pass

    def clean_student_id(self):
        pass

    def clean_grade(self):
        pass