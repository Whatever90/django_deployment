from django.conf.urls import url, include 
from . import views

def test(request):
	print "THIS IS WORKING!"

urlpatterns = [
	url(r'^$', views.index),
	url(r'^login$', views.login, name='login'),
	url(r'^registration$', views.registration, name='registration'),
	url(r'^dashboard$', views.dashboard, name='dashboard'),
	url(r'^logout$', views.logout, name='logout'),
	url(r'^addtocart/(?P<id>\d+)$', views.addtocart, name='addtocart'),
	url(r'^checkcart$', views.checkcart, name='checkcart'),
	url(r'^remove/(?P<id>\d+)$', views.remove, name='remove'),
	
	#u  # This line has changed!\
  ]
