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
	return render(request, "test_belt_app/index.html")
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
		create = Users.objects.create(name=request.POST['name'], email=request.POST['email'], password=encpw, gold=200)
		create.save()
		request.session['user'] = {
			'name': request.POST['name'],
			'id': create.id,
			'gold': create.gold,
			'log:': []
		}
		print request.session['user']
		print request.session['user']['gold']
		
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
			'gold': f.gold,
			'log': []
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
		'players' : Users.objects.all().order_by('-gold')[:3]
	}
	print request.session['user']['id']
	m = Users.objects.get(id=request.session['user']['id'])
	print m.activities
	return render(request, "test_belt_app/index2.html", context)


def logout(request):
	request.session['user'].clear()
	return redirect('/')

def game(request):
	print request.session['user']['id']
	#request.session['gold'] = request.session['user']['gold']
	#print request.session['user']['log']
	try:
		request.session['gold']
		print "Gold works!"
	except:
		request.session['user']['gold'] = 0
	try:
		request.session['log']
		print "Log works!"
	except:
		request.session['log'] = []
	context = {
		'logs': Logs.objects.filter(us=Users.objects.get(id=request.session['user']['id'])).order_by('-created_at')[:8],
		'user': Users.objects.get(id=request.session['user']['id'])
	}
	j = Logs.objects.all()
	print j
	return render(request,"test_belt_app/game.html", context)


def process(request):
	print "HELLO THERE! THIS IS PROCESS!"
	print '1'
	if request.POST['building'] == 'cave':
		z = random.randrange(-50, 25)
		if z>0:
			print z
			print "z greater than 0"
			request.session['gold'] += z
			new = Logs.objects.create(content="You've got "+str(z)+" gold in a cave...what ", us=Users.objects.get(id=request.session['user']['id']))
			new.save()
			#request.session['log'].append("You've got "+str(z)+" gold in a cave...what ")
		else:
			z = z*(-1)
			print z
			print "z lower than 0"
			request.session['gold'] -=z
			new = Logs.objects.create(content="Lol, Yeti sscrewed you up! You've lost "+str(z)+" gold ", us=Users.objects.get(id=request.session['user']['id']))
			#request.session['log'].append("Lol, Yeti sscrewed you up! You've lost "+str(z)+" gold ")
		print "cave"
		print '2'	
		

	if request.POST['building'] == 'farm':
		print "farm"
		z = random.randrange(-100, 50)
		print z
		if z>0:
			request.session['gold'] += z
			#request.session['log'].append("You've got "+str(z)+" gold in a farm...what a farmer!")
			new = Logs.objects.create(content="You've got "+str(z)+" gold in a farm...what a farmer!", us=Users.objects.get(id=request.session['user']['id']))
			new.save()
		else:
			z = z*(-1)
			request.session['gold'] -=z
			new = Logs.objects.create(content="You've got unlucky! Pay for your stupid cows "+str(z)+" gold", us=Users.objects.get(id=request.session['user']['id']))
			new.save()
			#request.session['log'].append("You've got unlucky! Pay for your stupid cows "+str(z)+" gold")
		print "farm"

	if request.POST['building'] == 'casino':
		z = random.randrange(-150, 75)
		print z
		if z>0:
			request.session['gold'] += z
			new = Logs.objects.create(content="You've won "+str(z)+" gold in a casino, good job!", us=Users.objects.get(id=request.session['user']['id']))
			new.save()
			#request.session['log'].append("You've won "+str(z)+" gold in a casino, good job!")
		else:
			z = z*(-1)
			request.session['gold'] -=z
			new = Logs.objects.create(content="Looser! Now give me your "+str(z)+" gold!", us=Users.objects.get(id=request.session['user']['id']))
			new.save()
			
			#request.session['log'].append("Looser! Now give me your "+str(z)+" gold!")
		print "casino"

	if request.POST['building'] == 'forest':
		request.session['gold'] += 50
		new = Logs.objects.create(content="You just have burried a dead body in a forrest. Well done. Here is your 50 gold. Come back if you need more money, we still have bunch of deads to get burried", us=Users.objects.get(id=request.session['user']['id']))
		new.save()
		#request.session['log'].append("You just have burried a dead body in a forrest. Well done. Here is your 50 gold. Come back if you need more money, we still have bunch of deads to get burried")
		#request.session['num'] = "NUM!!!"
		#for i in range(0, len(request.session['log']))
	print "you have", request.session['gold']
	#print request.session['log']
	return redirect('/game')
	
def endgame(request):
	request.session['user']['gold'] = request.session['gold']
	print "now you have", str(request.session['user']['gold'])
	#request.session['user']['log'].append(request.session['log'])
	del request.session['log']
	g = Users.objects.get(id=request.session['user']['id'])
	g.gold = request.session['user']['gold']
	#g.activities = request.session['user']['log']
	g.save()
	print "=============="
	print "XAXAAX YOUR MONEY", str(g.gold)
	print "=============="

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