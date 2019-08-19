from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add_book$',views.add_book),
    url(r'^sel_book$',views.sel_book),
    url(r'^update_book$',views.update_book),
    url(r'^del_book$',views.del_book),
]