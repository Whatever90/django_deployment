# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.shortcuts import render, redirect
import bcrypt
import re
from django.contrib import messages
from django.core.urlresolvers import reverse
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser
from django.contrib.auth import logout, login, authenticate
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
	print "we are in the main page"
	return render(request, "belt2_app/index.html")
# Create your views here.
def registration(request):
	#errors = User.objects.basic_validator(request.POST)
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
		#a = request.POST['dob']
##########
		try:
			a = parser.parse(request.POST['dob'])
		except:
			return redirect('/')
		print "+++++++++++++"
		print a.month
		#print relativedelta(datetime.now(), datetime.combine(a, datetime.min.time())).months 
		print "+++++++++++++"	

#########
		#print a.month
		#return redirect('/')
		create = Users.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=encpw, dob=request.POST['dob'])
		create.save()
		print 'shit'
		#login(request, request.POST['email'])
		request.session['user'] = {
			'name': request.POST['name'],
			'id': create.id,
			#'a': Friends.objects.create(add_by=Users.objects.get(id=request.session['user']['id']))
		}
		#print request.session['user']
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
			#user = authenticate(request, username=request.POST['login_email'], password=request.POST['login_password'])
			#login(request, user)
			request.session['user'] = {
			'name': f.name,
			'id': f.id,
			#'a': Friends.objects.create(add_by=Users.objects.get(id=request.session['user']['id']))
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

	print request.session['user']['id']
	try: 
		print "trying"
		context = {
			'you': Users.objects.get(id=request.session['user']['id']),
			'others': Users.objects.all(),#.exclude(addby=Users.objects.get(id=request.session['user']['id'])),
			'friends': Friends.objects.all().filter(add_by=Users.objects.get(id=request.session['user']['id']))
		}
		return render(request, "belt2_app/index2.html", context)
	except:
		print "failed"
		return redirect('/')
	
def user(request, id):
	context = {
		'user': Users.objects.get(id=id)
	}
	return render(request, "belt2_app/index3.html", context)

def addfriend(request, id):

	a = Friends.objects.create(add_by=Users.objects.get(id=request.session['user']['id']), added=Users.objects.get(id=id))
	#a.save()
	#print a.added.name
	#a = Users.objects.get(id=request.session['user']['id'])
	us = Users.objects.get(id=request.session['user']['id'])
	print us.name
	#a = Users.objects.get(id=id)
	lok = Users.objects.get(id=id)
	print lok.name
	#a.added.add(Users.objects.get(id=id))
	print a.added.id
	a.save()
	return redirect('/dashboard')


def remove(request, id):
	a = Friends.objects.get(add_by=Users.objects.get(id=request.session['user']['id']), added=Users.objects.get(id=id))
	a.delete()

	return redirect('/dashboard')

def logout(request):
	del request.session['user']
	#logout(request)
	return redirect('/')

