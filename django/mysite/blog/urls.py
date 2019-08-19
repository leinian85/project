from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^index$', views.index),
    url(r'^list$', views.list),
    url(r'^mypic$', views.mypic),
    url(r'^login$', views.login),
    url(r'^regist$', views.regist),
    url(r'^logout$', views.logout),
]