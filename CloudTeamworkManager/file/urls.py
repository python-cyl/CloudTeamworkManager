from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^picode/.*$', views.verify_code),
    url('img_test/', views.show_image),
    url(r'upload/', views.upload_image),
]