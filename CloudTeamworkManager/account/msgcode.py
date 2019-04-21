import urllib.request
import random
import time
import hashlib
import json


def get_headers():
    Nonce = str(random.randint(0, 9999999))
    AppKey = '26eea378260c9d92fc71ba2c19cc1790'
    CurTime = str(int(time.time()))
    CheckSum = hashlib.sha1(
        ("9b01db46b57a"+Nonce+CurTime).encode("utf-8")).hexdigest()
    headers = {'Nonce': Nonce,
               'AppKey': AppKey,
               'CurTime': CurTime,
               'CheckSum': CheckSum,
               'Content-Type': 'application/x-www-form-urlencoded'}
    return headers


def sendcode(mobile):
    url = 'https://api.netease.im/sms/sendcode.action'
    data = bytes(urllib.parse.urlencode({'mobile': mobile}), encoding='utf8')

    request = urllib.request.Request(url, data=data, headers=get_headers())
    response = urllib.request.urlopen(request)
    result = json.loads(response.read().decode("utf-8"))

    return result["code"]


def verifycode(mobile, code):
    url = 'https://api.netease.im/sms/verifycode.action'
    data = bytes(urllib.parse.urlencode(
        {'mobile': mobile, 'code': code}), encoding='utf8')
    request = urllib.request.Request(url, data=data, headers=get_headers())
    response = urllib.request.urlopen(request)
    result = json.loads(response.read().decode("utf-8"))

    return result["code"]

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
        result = sendcode(phone_number)
        # 发送验证码
        return HttpResponse(result)
        # 发送回执
    else:
        # 验证码校验失败
        return HttpResponse('412')