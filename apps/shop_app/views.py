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
	return render(request, "shop_app/index.html")
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
		create = Users.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=encpw, dob=request.POST['dob'], totalsum=0, money=0)
		create.save()
		#login(request, request.POST['email'])
		request.session['user'] = {
			'name': request.POST['name'],
			'id': create.id,
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
	#print 'we r in dashboard'
	try: 
		context = {
			'you': Users.objects.get(id=request.session['user']['id']),
			'len': len(Links.objects.all().filter(booked_by=Users.objects.get(id=request.session['user']['id']))),
			'items': Items.objects.all()
			
		}
		return render(request, "shop_app/index2.html", context)
	except:
		return redirect('/')
	
def addtocart(request, id):
	a = Links.objects.create(booked_by=Users.objects.get(id=request.session['user']['id']), booked=Items.objects.get(id=id))
	b = Users.objects.get(id=request.session['user']['id'])
	c = Items.objects.get(id=id)
	print c.price
	print b.totalsum
	b.totalsum += c.price
	b.save()
	return redirect('/dashboard')

def checkcart(request):
	context = {
		'you': Users.objects.get(id=request.session['user']['id']),
		'cartlen': len(Links.objects.all().filter(booked_by=Users.objects.get(id=request.session['user']['id']))),
		'items': Links.objects.all().filter(booked_by=Users.objects.get(id=request.session['user']['id'])),

	}
	return render(request, "shop_app/index4.html", context)
def remove(request, id):
	a = Links.objects.get(id=id)
	b = Users.objects.get(id=request.session['user']['id'])
	
	b.totalsum -= a.booked.price
	b.save()
	a.delete()
	#a.save()
	return redirect('/checkcart')

def logout(request):
	del request.session['user']
	#logout(request)
	return redirect('/')

