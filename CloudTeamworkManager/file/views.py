import os
import re
import json
from django.shortcuts import HttpResponse, render_to_response, render
from django.http import JsonResponse
from .verification_code import Code
from django.contrib.auth import logout
from PIL import Image, ImageFilter
from io import BytesIO
from guardian.decorators import permission_required_or_403
from guardian.shortcuts import assign_perm, remove_perm
from django.shortcuts import render
from django.http import FileResponse
from task.models import task
from file.models import appendix as _appendix


def verify_code(request):
    code = Code(4)
    string, code = code.make_code()
    request.session['verify'] = string
    print(request.session['verify'])
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
            return JsonResponse({"tip": "没有文件", "status": 400}, safe=False)

        destination = open(os.path.join("static/avatar/"+str(user_id)+'.jpg'), 'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()

        return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)


@permission_required_or_403('task.glance_over_task_details', (task, 'id', 'task_id'))
def appendix(request, task_id, file_name):
    if request.method == 'POST':
        _file = request.FILES.get("appendix")
        for a, b, filename in os.walk('./file/appendixes/%s'%task_id):
            if _file.name == filename:
                return JsonResponse({"tip": "文件已存在", "status": 400}, safe=False)

        file = open("./file/appendixes/%s/%s"%(task_id, _file.name), 'wb')
        for chunk in _file.chunks():
            file.write(chunk)
        file.close()
        file_size = os.path.getsize(".\\file\\appendixes\\%s\\%s" %(task_id, _file.name))
        file = _appendix.objects.create(filename=_file.name, task_id=task_id, publisher=request.user.id,filesize=file_size)
        target_task = task.objects.get(id = task_id)
        task_files = target_task.appendixes
        task_files = json.loads(task_files)
        task_files.append(file.id)
        task_files = json.dumps(task_files)
        target_task.appendixes = task_files
        target_task.save()

        assign_perm('file.edit_appendix', request.user, file)
        assign_perm('file.delete_appendix', request.user, file)

        return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)

    if request.method == 'GET':
        file = open("./file/appendixes/%s/%s" % (task_id, file_name), 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"'%file_name
        return response


def rename(request, task_id, appendix_id):
    target_task = task.objects.get(id = task_id)
    target_appendix = _appendix.objects.get(id = appendix_id)

    if request.user.has_perm("task.edit_appendix", target_task) or request.user.has_perm("file.edit_appendix", target_appendix):
        target_appendix_name = target_appendix.filename

        target_appendix.filename = request.POST.get("filename")
        target_appendix.save()

        os.rename('./file/appendixes/%s/%s' % (task_id, target_appendix_name), './file/appendixes/%s/%s' % (task_id, target_appendix.filename))

        return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
    return HttpResponse(status=403)


def delete(request, task_id, appendix_id):
    target_task = task.objects.get(id=task_id)
    target_appendix = _appendix.objects.get(id=appendix_id)

    if request.user.has_perm("task.delete_appendix", target_task) or request.user.has_perm("file.delete_appendix",target_appendix):
        target_appendix_name = target_appendix.filename
        _appendix.objects.filter(id=appendix_id).delete()
        path = './file/appendixes/%s/%s/'% (task_id,target_appendix_name)
        if os.path.exists(path):
            os.remove(path)

            return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
        return JsonResponse({"tip": "文件不存在", "status": 400}, safe=False)
    return HttpResponse(status=403)


def overlay(request, task_id, file_id):
    file = _appendix.objects.get(id=file_id)
    target_task = task.objects.get(id=task_id)
    if request.user.has_perm("task.edit_appendix", target_task) or request.user.has_perm("file.edit_appendix", target_appendix):
        HDD_file = open("./file/appendixes/%s/%s" % (task_id, file.filename), 'wb')
        _file = request.FILES.get("appendix")
        for chunk in _file.chunks():
            HDD_file.write(chunk)
        HDD_file.close()

        file_size = os.path.getsize("./file/appendixes/%s/%s" % (task_id, file.name))
        file.filesize = file_size
        file.save()
        return JsonResponse({"tip": "操作成功", "status": 200}, safe=False)
    return HttpResponse(status=403)
