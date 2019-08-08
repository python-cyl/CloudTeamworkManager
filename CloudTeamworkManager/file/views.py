import os
import re
from django.shortcuts import HttpResponse, render_to_response, render
from .verification_code import Code
from django.contrib.auth import logout
from PIL import Image, ImageFilter
from io import BytesIO


def verify_code(request):
    code = Code(4)
    string, code = code.make_code()
    request.session['verify'] = string
    print(request.session['verify'])
    # logout(request)
    # 清除本地session文件
    return HttpResponse(code.getvalue(), 'image/png')


def show_image(request):
    context = {}
    return render_to_response('show_img.html', context)


def upload_image(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        myFile = request.FILES.get('avatar', None)
        if not user_id:
            return HttpResponse('upload failed')
        if not myFile:
            return HttpResponse("no files for upload!")
        destination = open(os.path.join("static/img_for_user/"+user_id+'.jpg'), 'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()
        return HttpResponse("upload over!")
    return render(request, 'img_upload_for_user.html')


def show_img(request):
    if request.method == "GET":
        user_id = request.user.id
        if not user_id:
            return HttpResponse('用户未登录')
        else:
            a = open(os.path.join("static/img_for_user/"+user_id+'.jpg'), 'wb+')
            a.read()
            return HttpResponse(a)

def appendix(request, task_id, file_name):
    return HttpResponse("1200")