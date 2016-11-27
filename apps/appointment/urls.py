from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^add_appointment/(?P<user_id>\d+?)$', views.create_appointment),
    url(r'^delete/(?P<user_id>\d+?)$', views.delete),
    url(r'^edit/(?P<user_id>\d+?)$', views.edit)

]
