from django.conf.urls import url
from . import views

urlpatterns = [
    # http://127.0.0.1:8000/v1/users/
    url(r'^$', views.users),
    # APPEND_SLASH = False
    url(r'^/(?P<username>[\w]{1,30})$', views.users),
]
