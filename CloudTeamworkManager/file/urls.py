from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^picode/.*$', views.verify_code),
    path('image/<str:file_name>', views.show_image),
    path('avatar/', views.avatar),
    path('appendix/<int:task_id>/<str:file_name>', views.appendix),
]
