import re
from django.forms import ModelForm, ValidationError
from django.contrib.auth.models import User
from django import forms
from .models import task as models_task

class task(ModelForm):
    class Meta:
        model = models_task
        exclude = ("appendixes", "task_comment", "creator", "publish_data", "task_schedule", "task_progress", "all_members")

    def __init__(self, *args, **kwargs):
        super(task, self).__init__(*args, **kwargs)
        self.fields["deadline"].required = False
        self.fields["members"].required = False
        self.fields["task_description"].required = False
        self.fields["task_need"].required = False
        self.fields["leaders"].required = False

        self.fields["members"].initial = ""
        self.fields["leaders"].initial = ""
