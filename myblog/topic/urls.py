from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.topic),
    url(r'^(?P<username>[\w]{1,30})', views.topic),

]