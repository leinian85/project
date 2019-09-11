from django.conf.urls import url
from . import views


urlpatterns = [
    # http://127.0.0.1:8000/user/register
    url(r'^register$',views.register),
    url(r'^login$',views.login),
    url(r'^change/(?P<username>[\w]{1,11})$',views.change),
    url(r'^change_info/(?P<username>[\w]{1,11})$',views.change_info),
    url(r'^avatar/(?P<username>[\w]{1,11})$',views.avatar),
]