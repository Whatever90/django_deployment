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
	return render(request, "month_app/index.html")
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
		create = Users.objects.create(name=request.POST['name'], last_name=request.POST['last_name'], email=request.POST['email'], password=encpw, dob=request.POST['dob'], month=Monthes.objects.get(id=a.month))
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
	print 'we r in dashboard'
	context = {
		'monthes': Monthes.objects.all()
		
	}
	return render(request, "month_app/index2.html", context)


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
def game(request):
	
	context = {
		'logs': Logs.objects.filter(us=Users.objects.get(id=request.session['user']['id'])).order_by('-created_at')[:8],
		'user': Users.objects.get(id=request.session['user']['id'])
	}
	
	return render(request,"test_belt_app/game.html", context)


def process(request):
	asd = Users.objects.get(id=request.session['user']['id'])
	if request.POST['building'] == 'cave':
		z = random.randrange(-50, 25)
		if z>0:
			print z
			print "z greater than 0"
			asd.gold += z
			new = Logs.objects.create(content="You've got "+str(z)+" gold in a cave...what ", us=Users.objects.get(id=request.session['user']['id']))
			new.save()
			#request.session['log'].append("You've got "+str(z)+" gold in a cave...what ")
		else:
			z = z*(-1)
			print z
			print "z lower than 0"
			asd.gold -=z
			new = Logs.objects.create(content="Lol, Yeti sscrewed you up! You've lost "+str(z)+" gold ", us=Users.objects.get(id=request.session['user']['id']))
			#request.session['log'].append("Lol, Yeti sscrewed you up! You've lost "+str(z)+" gold ")
		print "cave"
		print '2'	
		

	if request.POST['building'] == 'farm':
		print "farm"
		z = random.randrange(-100, 50)
		print z
		if z>0:
			asd.gold += z
			#request.session['log'].append("You've got "+str(z)+" gold in a farm...what a farmer!")
			new = Logs.objects.create(content="You've got "+str(z)+" gold in a farm...what a farmer!", us=Users.objects.get(id=request.session['user']['id']))
			new.save()
		else:
			z = z*(-1)
			asd.gold -=z
			new = Logs.objects.create(content="You've got unlucky! Pay for your stupid cows "+str(z)+" gold", us=Users.objects.get(id=request.session['user']['id']))
			new.save()
			#request.session['log'].append("You've got unlucky! Pay for your stupid cows "+str(z)+" gold")
		print "farm"

	if request.POST['building'] == 'casino':
		z = random.randrange(-150, 75)
		print z
		if z>0:
			asd.gold += z
			new = Logs.objects.create(content="You've won "+str(z)+" gold in a casino, good job!", us=Users.objects.get(id=request.session['user']['id']))
			new.save()
			#request.session['log'].append("You've won "+str(z)+" gold in a casino, good job!")
		else:
			z = z*(-1)
			asd.gold -=z
			new = Logs.objects.create(content="Looser! Now give me your "+str(z)+" gold!", us=Users.objects.get(id=request.session['user']['id']))
			new.save()
			
			#request.session['log'].append("Looser! Now give me your "+str(z)+" gold!")
		print "casino"

	if request.POST['building'] == 'forest':
		asd.gold += 50
		new = Logs.objects.create(content="You just have burried a dead body in a forrest. Well done. Here is your 50 gold. Come back if you need more money, we still have bunch of deads to get burried", us=Users.objects.get(id=request.session['user']['id']))
		new.save()
		#request.session['log'].append("You just have burried a dead body in a forrest. Well done. Here is your 50 gold. Come back if you need more money, we still have bunch of deads to get burried")
		#request.session['num'] = "NUM!!!"
		#for i in range(0, len(request.session['log']))
	print "you have"
	
	# = request.session['user']['gold']
	asd.save()
	#print request.session['log']
	return redirect('/game')
	
def endgame(request):
	#request.session['user']['gold'] #= request.session['gold']
	

	return redirect('/dashboard')

def users(request, user_id):
	context = {
		'user': Users.objects.get(id=user_id)
	}
	return render(request, "test_belt_app/user.html", context)

def players(request):
	context = {
		'players': Users.objects.all().order_by("-gold")
	}
	return render(request, "test_belt_app/players.html", context)