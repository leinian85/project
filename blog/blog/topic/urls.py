from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    # 127.0.0.1/v1/tipocs/<author>
    url(r'^/(?P<username>[\w]{1,30})$', views.topics),
    url(r'^/(?P<username>[\w]{1,30})/topics$', views.topics),
    # 127.0.0.1/v1/tipocs?
]