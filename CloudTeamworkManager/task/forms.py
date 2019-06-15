import re
from django.forms import ModelForm, ValidationError
from django.contrib.auth.models import User
from django import forms
from .models import task

class task(ModelForm):
    class Meta:
        model = task
        exclude = ("publish_data", "task_status", "members_info", "task_schedule", "task_progress")