from CloudTeamworkManager.total_class import user, member, crew, leader, _publisher, task

def process(request, task_id):
    target_task = task(task_id = task_id)

    if request.method == "GET":
        return target_task.get_process(request)

    if request.method == "POST":
        return target_task.set_process(request)

def comment(request, task_id):
    target_task = task(task_id = task_id)

    if request.method == "GET":
        return target_task.get_comment(request, member_id)

    if request.method == "POST":
        return target_task.set_comment(request, member_id)
