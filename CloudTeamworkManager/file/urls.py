from django.urls import path
from . import views


urlpatterns = [
    path(r'^picode/.*$', views.verify_code),
    path('image/<str:file_name>', views.show_image),
    path('avatar/', views.avatar),
]
