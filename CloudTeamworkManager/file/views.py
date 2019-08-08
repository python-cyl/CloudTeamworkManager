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


def show_image(request, file_name):
    img = open(os.path.join("static/total/" + file_name), 'rb')
    return HttpResponse(img.read(), 'image/jpg')


def avatar(request):
    if not request.user.is_authenticated:
        return HttpResponse(status="403")

    if request.method == "GET":
        ava = open(os.path.join("static/avatar/"+str(user_id)+'.jpg'), 'rb')
        return HttpResponse(ava.read(), "image/jpg")

    if request.method == "POST":
        user_id = request.user.id
        myFile = request.FILES.get('avatar')

        if not myFile:
            return HttpResponse("no files for upload!")

        destination = open(os.path.join("static/img_for_user/"+str(user_id)+'.jpg'), 'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()

        return HttpResponse("upload over!")
    return render(request, 'img_upload_for_user.html')
