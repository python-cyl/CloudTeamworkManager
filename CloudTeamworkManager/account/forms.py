# 简单介绍一下forms.py。
# 这个文件中的表单类可以帮助我们快速处理表单，我们不仅可以自定义表单，还可以自定义校验规则，错误信息等
# 表单分为两大类，继承forms.Form的表单和继承ModelForm的表单。
# 这个文件中的例子和注释可以帮你快速入门

import re
from django.forms import ModelForm, ValidationError
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile
from .msgcode import verifycode


def my_clean_phone_number(phone_number):
    if re.match("^1[34578]\d{9}$", phone_number):
        try:
            User.objects.get(username = phone_number)
            raise ValidationError("手机号码已被注册")
        except User.DoesNotExist:
            return phone_number
    raise ValidationError("手机号码不正确")

def my_clean_picode(picode, answer):
        if re.match("\\w{4}", picode):
            if picode.upper() == answer.upper():
                return picode
            raise ValidationError("验证码校验失败")
        raise ValidationError("验证码格式错误")

# 这是一个继承forms.Form类的表单
# 这类表单的字段需要自己编写，不能从模型中继承
class RegisterForm(forms.Form):
    # 这是定义这个表单的字段
    phone_number = forms.CharField(max_length=11, min_length=11, label="手机号")
    password = forms.CharField(max_length=16, min_length=6, label="密码")
    picode = forms.CharField(max_length=4, min_length=4, label="图形验证码")
    msgcode = forms.CharField(max_length=4, min_length=4, label="短信验证码")

    # 这个成员属性用于临时存储图形验证码的答案。
    # answer属性会在该类在views.py中实例化后赋值，用于核对图形验证码。
    # 这样做的原因是：一般情况下，仅可以通过对request相关方法的调用才能获取验证码的答案，
    # 但是该类在创建时并不会获取到request，因此无法在类内获取验证码答案。
    # 正是由于无法再类内获取答案，才只能在该类在views.py中实例化后有views.py中的相关代码赋值。
    answer = ""

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]

        # 这个函数定义在该文件开头，用于核对手机号
        return my_clean_phone_number(phone_number)

    def clean_msgcode(self):
        msgcode = self.cleaned_data["msgcode"]

        if re.match("\d{4}", msgcode):

            # if verifycode(self.cleaned_data.get("phone_number", "11111111111"), msgcode) == 200:            
            # 这里关闭了短信验证码的校验功能，上一行代码是开启时的代码
            if verifycode(self.cleaned_data.get("phone_number"), msgcode):
                return msgcode
            raise ValidationError("验证码校验失败")
        else:
            raise ValidationError("验证码格式错误")

    def clean_picode(self):
        picode = self.cleaned_data["picode"]

        return my_clean_picode(picode, self.answer)

class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=11, min_length=11, label="手机号")

    def clean_phone_number(self):
        return my_clean_phone_number(self)

class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11, min_length=11, label="手机号")
    password = forms.CharField(max_length=16, min_length=6, label="密码")

class GetPasswordForm(forms.Form):
    phone_number = forms.CharField(max_length=11, min_length=11, label="手机号")
    password = forms.CharField(max_length=16, min_length=6, label="新密码")
    picode = forms.CharField(max_length=4, min_length=4, label="图形验证码")
    msgcode = forms.CharField(max_length=4, min_length=4, label="短信验证码")
    answer = ""

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")

        if re.match("^1[34578]\d{9}$", phone_number):
            try:
                User.objects.get(username = phone_number)
            except User.DoesNotExist:
                raise ValidationError("手机号码未注册")
            return phone_number
        raise ValidationError("手机号码不正确")

    def clean_msgcode(self):
        msgcode = self.cleaned_data["msgcode"]

        if re.match("\d{4}", msgcode):
            if verifycode(self.cleaned_data.get("phone_number"), msgcode):
                return msgcode
            raise ValidationError("验证码校验失败")
        raise ValidationError("验证码格式错误")

    def clean_picode(self):
        picode = self.cleaned_data["picode"]

        if re.match("\\w{4}", picode):
            if picode.upper() == self.answer.upper():
                return picode
            raise ValidationError("验证码校验失败")
        raise ValidationError("验证码格式错误")

# 这是典型的继承ModelForm的form表单
class extend_info(ModelForm):
    class Meta:

        # 这一行指定这个form表单来自UserProfile模型
        model = UserProfile

        # 这一行排除了模型中指定的几个字段
        exclude = ("involved_projects_number", "management_projects", "unread_notifications", "read_notifications", "involved_projects", "user")
        
        #除了排除模型中的指定字段，还可以指定仅包含模型中的指定字段，指定label等
        
    # __init__()函数是类的初始化函数。在此用于初始化表单
    def __init__(self, *args, **kwargs):

        # 这一行实例化父类对象
        super(extend_info, self).__init__(*args, **kwargs)

        # 这三行将该表单的三个字段设置为非必填项目
        # 非必填项目对应必填项目，不填写必填项目，表单无法提交
        self.fields["home_address"].required = False
        self.fields["guardian_phone"].required = False
        self.fields["introduction"].required = False

    # 这是自定义表单校验函数，函数名为"clean_" + "字段名"
    def clean_email(self):

        # form表单的内容会先使用内置的校验函数校验，然后将结果存储在 self.cleaned_data 中。
        # 这里获取内置校验函数校验的结果，对结果进行自定义校验
        email = self.cleaned_data.get("email")

        if re.match("^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$", email):
            
            # 如果校验成功，直接返回校验后的结果（或整理后的结果）
            return email
        else:
            
            # 如果电子邮箱校验失败，抛出错误："电子邮箱不正确"，这个错误可以被用户看到
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

# 这个类继承上一个类，仅修改了排除的字段，其他内容没有更改
# 继承extend_info是因为用户变更信息的表单与第一次填写信息的表单的唯一区别是：变更信息的表单缺少姓名等不允许修改的字段
class change_info(extend_info):
    class Meta:
        model = UserProfile
        exclude = ("name", "student_id", "cloud_id", "magor", "grade", "sex", "management_projects", "unread_notifications", "read_notifications", "involved_projects", "user")
