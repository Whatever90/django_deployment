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
	url(r'^$', views.index),
	url(r'^login$', views.login, name='login'),
	url(r'^registration$', views.registration, name='registration'),
	url(r'^dashboard$', views.dashboard, name='dashboard'),
	url(r'^logout$', views.logout, name='logout'),
	url(r'^game$', views.game, name='game'),
	url(r'^process$', views.process, name='process'),
	url(r'^endgame$', views.endgame, name='endgame'),
	url(r'^players$', views.players, name='players'),
	url(r'^newhero$', views.newhero, name='newhero'),
	url(r'^newpower$', views.newpower, name='newpower'),
	url(r'^createhero$', views.createhero, name='createhero'),
	url(r'^createpower$', views.createpower, name='createpower'),
	url(r'^like/(?P<hero_id>\d+)$', views.likehero, name='likehero'),
	url(r'^unlike/(?P<hero_id>\d+)$', views.unlikehero, name='unlikehero'),
	url(r'^hero/(?P<hero_id>\d+)$', views.hero, name='hero'),
	#url(r'^specage/(?P<num>\d+)$', views.specage, name='specage'),
	#url(r'^message$', views.message, name='message'),
	#url(r'^books/adding$', views.adding, name='adding'),
	#url(r'^books/(?P<book_id>\d+)$$', views.book, name='book'),
	#url(r'^users/(?P<user_id>\d+)$$', views.user, name='user'),
	#url(r'^delete/(?P<rev_id>\d+)$', views.delete, name='delete'),
	#url(r'^books$', views.dashboard, name='dashboard'),
	#url(r'^destroy_confirm/(?P<user_id>\d+)$', views.destroy_confirm, name='destroy_confirm'),
	url(r'^(?P<user_id>\d+)$', views.users, name='users'), 
	#url(r'^users/created$', views.created, name='created'),
	#url(r'^(?P<user_id>\d+)/edit$', views.edit, name='edit'),
	#url(r'^(?P<user_id>\d+)/edited$', views.edited, name='edited'),
	#u  # This line has changed!\
  ]
