from django.urls import path
from . import views


urlpatterns = [
    #path('get_permission/', views.get_permission_page),
    #path("add_tasks_page/", views.add_tasks_page),
    #path("check_permission_page/<need>/", views.check_permission_page),
    path("create_task/", views.create_task),
    path('get_members/', views.get_members),
    path('upgrade_process/', views.upgrade_process),
    path('edit_task/', views.edit_task),
]
