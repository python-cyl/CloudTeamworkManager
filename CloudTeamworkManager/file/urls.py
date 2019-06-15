from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^picode/.*$', views.verify_code),
]