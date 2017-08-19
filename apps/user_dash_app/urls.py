"""main_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include 
from . import views

def test(request):
	print "THIS IS WORKING!"

urlpatterns = [
	url(r'^$', views.welcomen),
	url(r'^index$', views.index, name='index'),
	url(r'^dashboard$', views.dashboard, name='dashboard'),
	url(r'^login$', views.login, name='login'),
	url(r'^registration$', views.registration, name='registration'),
	url(r'^new$', views.new, name='new'),
	url(r'^user/(?P<user>\d+)$', views.user, name='user'),
	url(r'^user/(?P<user>\d+)/post$', views.post, name='post'),
	url(r'^user/(?P<user>\d+)/comment/(?P<post>\d+)$', views.comment, name='comment')
	#url(r'^destroy_confirm/(?P<user_id>\d+)$', views.destroy_confirm, name='destroy_confirm'),
	#url(r'^(?P<user_id>\d+)$', views.users, name='users'), 
	#url(r'^users/created$', views.created, name='created'),
	#url(r'^(?P<user_id>\d+)/edit$', views.edit, name='edit'),
	#url(r'^(?P<user_id>\d+)/edited$', views.edited, name='edited'),
	#u  # This line has changed!\
  ]
