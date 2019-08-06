from django.urls import path
from .views import comment, progress

urlpatterns = [
    path('process/<int:task_id>', views.process),
    path('comment/<int:task_id>', views.comment),
    ]
