from django.conf.urls import include, url
from django.views.generic import RedirectView
from django.contrib.auth import *
from . import views

app_name = 'proc'
urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/proc/home', permanent=True)),
    url(r'^register/$', views.register, name='register'),
    url(r'^sucess/$', views.register_sucessed, name="sucsess"),
    url(r'^home/$', views.home, name="home"),
    url(r'^login/$', views.login_user, name="login"),
    # url(r'^logout/$', views.register, name="logout"),
    url(r'^medicine/$', views.medicine_manager, name="medicine_manager"),
    url(r'^medicineregister/$', views.medicine_register, name="medicineregister"),
    url(r'^medicine_registered/$', views.medicine_show, name="medicine_registered"),
    url(r'^medicine_delete/(?P<id>\d+)/$', views.medicine_delete, name="medicine_delete"),
    url(r'^medicineupdate/(?P<id>\d+)/$', views.medicine_update, name="medicineupdate"),
    url(r'^medicine_search/$',views.medicine_search,name="medicinesearch"),
    url(r'^medicine_results/(?P<nome>[\w\-]]+)/$',views.medicine_results,name="medicineresults"),
    url(r'^patientregister/(?P<id>\d+)/$', views.patient_register, name="patientregister"),
    url(r'^patient_registered/$', views.patient_show, name="patient_registered"),
    url(r'^patient_delete/(?P<id>\d+)/$', views.patient_delete, name="patient_delete"),
    url(r'^patientupdate/(?P<id>\d+)/$', views.patient_update, name="patientupdate"),
    # url(r'^registerpat/$',views.registerpat, name= "registerpat")
]
