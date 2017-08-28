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
#from .forms import RegisterForm, LoginForm
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
	print "we are in the main page"
	
	return render(request, "belt3_app/index.html")
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
		create = Users.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=encpw)
		create.save()
		print 'sh1t'
		request.session['user'] = {
			'name': request.POST['name'],
			'id': create.id,
		}
		
		
		return redirect('/travels')
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
			'id': f.id
			}

			return redirect('/travels')
		else:
			print 'password failed'
			request.session['err'] += 'wrong login and/or password'
			return redirect('/')
	except:
		print 'failed to login'
		request.session['err'] += 'wrong login and/or password'
		return redirect('/')

def travels(request):
	print 'we r in dashboard'
	try: 
		print request.session['user']['id']
		print "trying"
		
		context = {
			'you': Users.objects.get(id=request.session['user']['id']),
			'trips': Trips.objects.all().exclude(user=Users.objects.get(id=request.session['user']['id'])),
			
		}
		return render(request, "belt3_app/index2.html", context)
	except:
		print "failed"
		return redirect('/')


def add(request):
	print 'we r in add'
	try: 
		print request.session['user']['id']
		print "trying"
		
		return render(request, "belt3_app/index3.html")
	except:
		print "failed"
		return redirect('/')

def addtrip(request):
	try:
		print request.session['user']['id']
		results = Trips.objects.tripvalidator(request.POST)
		
		if len(results['errors']) > 0:
			for error in results['errors']:
				messages.error(request, error)
			return redirect('/add')
		else:
			a = Trips.objects.create(destination=request.POST['dest'], desc=request.POST['desc'],planned_by=Users.objects.get(id=request.session['user']['id']),datefrom=request.POST['datefrom'],dateto=request.POST['dateto'])
			a.user.add(Users.objects.get(id=request.session['user']['id']))
			return redirect('/travels')
	except:
		print "failed"
		return redirect('/')

def join(request, id):
	try:
		print request.session['user']['id']
		a = Trips.objects.get(id=id)
		a.user.add(Users.objects.get(id=request.session['user']['id']))
		return redirect('/travels')
	except:
		print "failed"
		return redirect('/')
	

def destination(request, id):
	print 'we r in dest'
	try: 
		print request.session['user']['id']
		print "trying"
		context = {
		'trip': Trips.objects.get(id=id)
		}
		return render(request, "belt3_app/index4.html", context)
	except:
		print "failed"
		return redirect('/')
	
	

def logout(request):
	del request.session['user']
	#logout(request)
	return redirect('/')

