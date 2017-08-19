# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.shortcuts import render, redirect
import bcrypt
import re
from django.contrib import messages
from django.core.urlresolvers import reverse

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#not EMAIL_REGEX.match(request.form['email']):
def welcomen(request):
	return render(request, "user_dash_app/welcome.html")
def index(request):
	request.session['context'] = {}
	context = {
		"user": Users.objects.all(),
		}
	print "we are in log/reg page"
	return render(request, "user_dash_app/index.html", context)
def dashboard(request):
	context = {
		"Users": Users.objects.all(),
		}
	print "we are in dashboard page"
	return render(request, "user_dash_app/dashboard.html", context)
def registration(request):
	return render(request, "user_dash_app/registration.html")
def new(request):
	#errors = User.objects.basic_validator(request.POST)
	request.session['err'] = ''
	request.session['error'] = ""
	encpw = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt())
	encpw2 = bcrypt.hashpw(request.POST.get('confirm').encode(), bcrypt.gensalt())
	results = Users.objects.basic_validator(request.POST)
	if results['status'] == False:
		for error in results['errors']:
			messages.error(request, error)
		return redirect('/registration')
	
	else:
		print "everything is alright"
		create = Users.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], desc=request.POST['desc'], password = encpw, level = 1)
		create.save()
		if create.id == 1:
			create.level = 2
			create.save()
		request.session['context'] = {
			'name': request.POST['first_name'],
			'action': 'registered',
			'id': create.id 
		}
		
		return redirect('/dashboard')
	print "created a new course"
	
	
	return redirect('/registration')

def login(request):
	print "hey dude login"
	request.session['error'] = ""
	request.session['err'] = ''
	print request.POST['login_email']
	#print Users.objects.login(request.POST)
	try: 
		print 'trying'
		f = Users.objects.get(email=request.POST['login_email'])
		print f.first_name
		if bcrypt.checkpw(request.POST['login_password'].encode(), f.password.encode()): #f.password == bcrypt.hashpw(.encode(), bcrypt.gensalt()):
			print "Correct"
			request.session['context'] = {
			'name': f.first_name,
			'action': 'loggedin',
			'id': f.id 
		}
			return redirect('/dashboard')
		else:
			print 'password failed'
			request.session['err'] += 'wrong login and/or password'
			return redirect('/index')
	except:
		print 'failed to login'
		request.session['err'] += 'wrong login and/or password'
		return redirect('/index')

def user(request, user):
	x = Users.objects.get(id=user)
	request.session['user_name'] = x.first_name
	request.session['user_last'] = x.last_name
	request.session['user_id'] = x.id
	request.session['reg'] = str(x.created_at)
	request.session['email'] = x.email
	request.session['desc'] = x.desc
	a = Posts.objects.filter(postedto=Users.objects.get(id=x.id))
	print a
	context = {
		'posts': Posts.objects.filter(postedto=Users.objects.get(id=x.id)),
		#'comments': Comments.objects.filter(postedto=Posts.objects.filter(postedto=Users.objects.get(id=x.id)))
	}
	return render(request, "user_dash_app/user.html", context)

def post(request, user):
	print request.POST['message']
	print request.session['context']['id']
	q = Users.objects.get(id=user)
	print q.first_name
	createpost = Posts.objects.create(postedto=Users.objects.get(id=user), poster=Users.objects.get(id=request.session['context']['id']), post=request.POST['message'])
	createpost.save()
	Posts.objects.all()
	return redirect(reverse('user', kwargs={'user': user}))

def comment(request, user, post):
	print request.POST['comment']
	print "checking comments"
	print "+++++++"
	print post
	print "+++++++"
	#print user
	z = Comments.objects.create(postedto=Posts.objects.get(id=post), poster=Users.objects.get(id=request.session['context']['id']), comment=request.POST['comment'])
	#z.save()
	return redirect(reverse('user', kwargs={'user': user}))
def destroy_confirm(request, user):
	print "terminating course"
	destroy = Course.objects.get(id=user)
	#print destroy.first_name
	destroy.delete()
	return redirect('/')


# Create your views here.
