# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.shortcuts import render, redirect
import bcrypt
import re
from django.contrib import messages
from django.core.urlresolvers import reverse
import random
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
	print "we are in the main page"
	return render(request, "hero_app/index.html")

def registration(request):
	errors = User.objects.basic_validator(request.POST)
	request.session['err'] = ''
	request.session['error'] = ""
	print request.POST['name']
	results = Users.objects.basic_validator(request.POST)
	if results['status'] == False:
		for error in results['errors']:
			messages.error(request, error)
		return redirect('/')
	
	else:
		print "everything is alright"
		encpw = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt())
		create = Users.objects.create(name=request.POST['name'], email=request.POST['email'], password=encpw)
		create.save()
		request.session['user'] = {
			'name': request.POST['name'],
			'id': create.id,
		}
		print request.session['user']
		#print request.session['user']['gold']
		
		return redirect('/dashboard')
	#print "created a new course"
	return redirect('/')
def login(request):
	print "hey dude login"
	request.session['error'] = ""
	request.session['err'] = ''
	print request.POST['login_email']
	x = request.POST['login_email']
	#print Users.objects.login(request.POST)
	try: 
		print 'trying'
		f = Users.objects.get(email=x)
		print f.name
		print f.password
		print request.POST['login_password'].encode()
		if bcrypt.checkpw(request.POST['login_password'].encode(), f.password.encode()): #f.password == bcrypt.hashpw(.encode(), bcrypt.gensalt()):
			print "Correct"
			request.session['user'] = {
			'name': f.name,
			'id': f.id,
			}

			return redirect('/dashboard')
		else:
			print 'password failed'
			request.session['err'] += 'wrong login and/or password'
			return redirect('/')
	except:
		print 'failed to login'
		request.session['err'] += 'wrong login and/or password'
		return redirect('/')

def dashboard(request):
	print 'we r in dashboard'
	context = {
		'heroes' : heroes.objects.all().order_by('-name'),
		'power': powers.objects.all(),
		'user': Users.objects.get(id=request.session['user']['id'])
		
	}
	return render(request, "hero_app/index2.html", context)


def logout(request):
	request.session['user'].clear()
	return redirect('/')

def newhero(request):
	context = {
		'powers' : powers.objects.all()
	}
	return render(request, "hero_app/addhero.html", context)

def createhero(request):
	print "creating a hero!"
	print request.POST['power']
	name = request.POST['heroname']
	new = heroes.objects.create(name=name, user=Users.objects.get(id=request.session['user']['id']), power=powers.objects.get(id=request.POST['power']), like=0)
	new.save()
	return redirect('/dashboard')

def newpower(request):
	print request.session['user']['id']
	context = {
		'powers' : powers.objects.all()
	}
	return render(request, "hero_app/addpower.html", context)

def createpower(request):
	print "creating a power!"
	name = request.POST['powername']
	print request.POST['powerdesc']
	new = powers.objects.create(name=name, desc = request.POST['powerdesc'])
	new.save()
	return redirect('/dashboard')

def likehero(request, hero_id):
	us = Users.objects.get(id=request.session['user']['id'])
	print us.name
	a = heroes.objects.get(id=hero_id)
	a.like +=1
	a.liked_by.add(Users.objects.get(id=request.session['user']['id']))
	a.save()
	return redirect('/dashboard')

def unlikehero(request, hero_id):
	us = Users.objects.get(id=request.session['user']['id'])
	print us.name
	a = heroes.objects.get(id=hero_id)
	a.like -=1
	a.liked_by.remove(Users.objects.get(id=request.session['user']['id']))
	a.save()
	return redirect('/dashboard')


def hero(request, hero_id):
	context = {
		'hero': heroes.objects.get(id=hero_id),
		'user': Users.objects.get(id=request.session['user']['id'])
	}
	a = heroes.objects.get(id=hero_id)
	print '+++++++++++++++++++'
	print a.liked_by.all().values()
	print "--------------------0"
	f = Users.objects.get(id=request.session['user']['id'])
	print f.id
	print "+++++++++++++++++++"
	return render(request, "hero_app/hero.html", context)

#####################################################################################
#####################################################################################
#####################################################################################

