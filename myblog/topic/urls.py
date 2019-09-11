from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.topic),
    url(r'^(?P<username>[\w]{1,11})', views.topic),
    url(r'^release/(?P<username>[\w]{1,11})', views.release),

]