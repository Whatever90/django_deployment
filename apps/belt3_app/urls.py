from django.conf.urls import url, include 
from . import views

def test(request):
	print "THIS IS WORKING!"

urlpatterns = [
	url(r'^$', views.index),
	url(r'^login$', views.login, name='login'),
	url(r'^registration$', views.registration, name='registration'),
	url(r'^travels$', views.travels, name='travels'),
	url(r'^logout$', views.logout, name='logout'),
	url(r'^destination/(?P<id>\d+)$', views.destination, name='destination'),
	url(r'^add$', views.add, name='add'),
	url(r'^addtrip$', views.addtrip, name='addtrip'),
	url(r'^join/(?P<id>\d+)$', views.join, name='join'),
	#url(r'^remove/(?P<id>\d+)$', views.remove, name='remove'),
	
	#u  # This line has changed!\
  ]
