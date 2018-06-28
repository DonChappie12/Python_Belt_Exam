from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^addJob$', views.addJob),
    url(r'^createJob$', views.createJob),
    url(r'^view/(?P<job_id>\d+)$', views.view),
    url(r'^edit/(?P<job_id>\d+)$', views.edit),
    url(r'^edit/(?P<job_id>\d+)/update$', views.update),
    url(r'^join/(?P<job_id>\d+)$', views.join),
    url(r'^delete/(?P<job_id>\d+)$', views.delete)
]