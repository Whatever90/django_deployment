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
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
	print "we are in the main page"
	return render(request, "poke_app/index.html")
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
		a = parser.parse(request.POST['dob'])
		print "+++++++++++++"
		print a.month
		#print relativedelta(datetime.now(), datetime.combine(a, datetime.min.time())).months 
		print "+++++++++++++"	

#########
		#print a.month
		#return redirect('/')
		create = Users.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=encpw, dob=request.POST['dob'], pokesum=0)
		create.save()
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
	context = {
		'you': Users.objects.get(id=request.session['user']['id']),
		'users': Users.objects.all().exclude(id=request.session['user']['id']),
		'beingpoked': Pokes.objects.all().filter(poked=Users.objects.get(id=request.session['user']['id'])).order_by('-pokesum'),
		'len': len(Pokes.objects.all().filter(poked=Users.objects.get(id=request.session['user']['id'])))
		
	}
	return render(request, "poke_app/index2.html", context)

def poke(request, id):
	print id
	a = Users.objects.get(id=id)
	print a.name
	a.pokesum +=1
	a.save()
	if Pokes.objects.all().filter(poked=Users.objects.get(id=id),poked_by=Users.objects.get(id=request.session['user']['id'])):
		print "Yep, he is here!"
		g = Pokes.objects.get(poked=Users.objects.get(id=id), poked_by=Users.objects.get(id=request.session['user']['id']))
		print g.id
		g.pokesum+=1
		g.save()
	else:	
		print "failed"
		f = Pokes.objects.create(poked=Users.objects.get(id=id), poked_by=Users.objects.get(id=request.session['user']['id']), pokesum=1)
	#print a.pokd.all().values()
	print "+++++++++++++++"
	#print len(Pokes.objects.all().filter(poked=Users.objects.get(id=id)))
	print "+++++++++++++++"


	return redirect('/dashboard')


def logout(request):
	request.session['user'].clear()
	return redirect('/')

