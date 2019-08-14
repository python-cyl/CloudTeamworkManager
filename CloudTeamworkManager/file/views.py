import os
import re
from django.shortcuts import HttpResponse, render_to_response, render
from .verification_code import Code
from django.contrib.auth import logout
from PIL import Image, ImageFilter
from io import BytesIO
from guardian.decorators import permission_required_or_403
from guardian.shortcuts import assign_perm, remove_perm
from django.shortcuts import render
from django.http import FileResponse
from task.models import task
from file.models import appendix


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

        destination = open(os.path.join("static/avatar/"+str(user_id)+'.jpg'), 'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()

        return HttpResponse("upload over!")
    return render(request, 'img_upload_for_user.html')

  
@permission_required_or_403('task.glance_over_task_details', (task, ('id', 'task_id')))
def appendix(request, task_id, file_name):
    if request.method == 'POST':
        _file = request.FILES.get("appendix")
        for a,b,filename in os.walk('./file/appendixes/%s'%task_id):
            if _file.name == filename:
                if not request.user.has_perm('file.edit_appendix', appendix.objects.get(filename = filename)):
                    return HttpResponse("403")

        file = open("./file/appendixes/%s/%s"%(task_id, _file.name), 'wb')
        file.write(_file.read())
        file.close()
        file = appendix.objects.create(filename='_file.name',task_id='task_id',publisher=request.user.id)
        assign_perm('file.edit_appendix', request.user, file)
        assign_perm('file.delete_appendix', request.user, file)

        return HttpResponse("200")

    if request.method == 'GET':
        file = open("./file/appendixes/%s/%s" % (task_id, file_name), 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"'%file_name
        return response


def upload(request):
    return render(request, "upload.html")


def rename_appendix(request, task_id, appendix_id):
    target_task = task.objects.get(id = task_id)
    target_appendix = appendix.objects.get(id = appendix_id)

    if request.user.has_perm("task.edit_appendix", target_task) or request.user.has_perm("file.edit_appendix", target_appendix):
        target_appendix_name = target_appendix.filename

        target_appendix.filename = request.POST.get("filename")
        target_appendix.save()

        os.rename('./file/appendixes/%s/%s' % (task_id, target_appendix_name), './file/appendixes/%s/%s' % (task_id, target_appendix.filename))

        return HttpResponse("200")
    return HttpResponse(status=403)


def delete(request,task_id,appendix_id):
    target_task = task.objects.get(id=task_id)
    target_appendix = appendix.objects.get(id=appendix_id)

    if request.user.has_perm("task.delete_appendix", target_task) or request.user.has_perm("file.delete_appendix",target_appendix):
        target_appendix_name = target_appendix.filename
        appendix.objects.filter(id=appendix_id).delete()
        path = './file/appendixes/%s/%s/'% (task_id,target_appendix_name)
        if os.path.exists(path):
            os.remove(path)

            return HttpResponse("200")
        return HttpResponse("file does not exist")
    return HttpResponse(status=403)
