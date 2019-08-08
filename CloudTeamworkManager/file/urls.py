from django.urls import path
from . import views


urlpatterns = [
    path(r'^picode/.*$', views.verify_code),
    path('img_test/', views.show_image),
    path('upload/', views.upload_image),
]
