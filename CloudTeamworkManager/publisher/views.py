from CloudTeamworkManager.total_class import user, member, crew, leader, _publisher, task

def task_progress(request, task_id):
    target_task = task(task_id = task_id)

    if request.method == "GET":
        return target_task.get_progress(request)

    if request.method == "POST":
        return target_task.edit_progress(request)

def task_comment(request, task_id):
    target_task = task(task_id = task_id)

    if request.method == "GET":
        return target_task.get_comment(request)

    if request.method == "POST":
        return target_task.edit_comment(request)

def task_shedule(request, task_id):
    target_task = task(task_id = task_id)

    if request.method == "GET":
        return target_task.get_shedule(request)

    if request.method == "POST":
        return target_task.get_shedule(request)

def personal_comments(request, task_id, member_id):
    target_task = task(task_id = task_id)
    target_user = member(user_id = member_id, target_task = target_task.task)

    if request.method == "GET":
        return target_user.view_personal_comments(request)

    if request.method == "POST":
        return target_user.edit_personal_comments(request)

def personal_shedule(request, task_id, member_id):
    target_task = task(task_id = task_id)
    target_user = member(user_id = member_id, target_task = target_task.task)

    if request.method == "GET":
        return target_user.view_personal_shedule(request)

    if request.method == "POST":
        return target_user.edit_personal_shedule(request)

def personal_progress(request, task_id, member_id):
    target_task = task(task_id = task_id)
    target_user = member(user_id = member_id, target_task = target_task.task)

    if request.method == "GET":
        return target_user.view_personal_progress(request)

    if request.method == "POST":
        return target_user.edit_personal_progress(request)
