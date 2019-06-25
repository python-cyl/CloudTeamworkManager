from django.urls import path
from . import views


urlpatterns = [
    path("create_task/", views.create_task),
    path('edit_task/<int:task_id>', views.edit_task),
    path('delete_task/<int:task_id>', views.delete_task),
    path('get_members/', views.get_members),
    path('process/<int:task_id>', views.process),
    path('task_page/<int:task_id>', views.delete_task),
]
