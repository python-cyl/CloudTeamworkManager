from django.urls import path
from . import views
pass

urlpatterns = [
    path(r'^picode/.*$', views.verify_code),
    path('image/<str:file_name>', views.show_image),
    path('avatar/', views.avatar),
    path('appendix/<int:task_id>/<str:file_name>', views.appendix),
    path("upload/", views.upload),
]
