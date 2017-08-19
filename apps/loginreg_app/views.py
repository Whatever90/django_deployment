# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import User
from django.shortcuts import render, redirect
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#not EMAIL_REGEX.match(request.form['email']):
def index(request):
	print "we are in log/reg page"
	return render(request, "user_dash_app/index.html")

def new(request):
	#errors = User.objects.basic_validator(request.POST)
	request.session['err'] = ''
	request.session['error'] = ""
	encpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
	encpw2 = bcrypt.hashpw(request.POST['confirm'].encode(), bcrypt.gensalt())
	
	if request.POST['password']!=request.POST['confirm']:
		print "password failed"
		request.session['error'] += '<p>Failed to confirm the password</p>'
		#return redirect('/')
	if len(request.POST['first_name']) <3:
		print "first_name failed"
		request.session['error'] += '<p>First name should be not fewer than 3 characters</p>'
		#return redirect('/')
	if len(request.POST['last_name']) <3:
		print "last name failed"
		request.session['error'] += '<p>Last name should be not fewer than 3 characters</p>'
		#return redirect('/')
	if not EMAIL_REGEX.match(request.POST['email']):
		print "email failed"
		request.session['error'] += '<p>Email should be right format</p>'
		#return redirect('/')
	if len(request.POST['password'])<8:
		print "password failed"
		request.session['error'] += '<p>Password should be not fewer that 8 characters</p>'
	if len(request.session['error'])>0:
		return redirect('/')
	else:
		print "everything is alright"
		create = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password = encpw, confirm_password=encpw2)
		create.save()
		content = {
			'name': request.POST['first_name'],
			'action': 'registered' 
		}
		request.session['error'] = ''
		request.session['err'] = ''
		return render(request, 'loginreg_app/index2.html', content)
	print "created a new course"
	
	
	return redirect('/')

def login(request):
	print "hey dude login"
	request.session['error'] = ""
	request.session['err'] = ''
	try: 
		User.objects.get(email=request.POST['login_email'])
		f = User.objects.get(email=request.POST['login_email'])
		print f.first_name
		if bcrypt.checkpw(request.POST['login_password'].encode(), f.password.encode()): #f.password == bcrypt.hashpw(.encode(), bcrypt.gensalt()):
			print "Correct"
			content = {
			'name': f.first_name,
			'action': "logged in"
			}
			return render(request, 'loginreg_app/index2.html', content)
		else:
			request.session['err'] += 'wrong login and/or password'
			return redirect('/')
	except:
		request.session['err'] += 'wrong login and/or password'
		return redirect('/')
def destroy_confirm(request, user_id):
	print "terminating course"
	destroy = Course.objects.get(id=user_id)
	#print destroy.first_name
	destroy.delete()
	return redirect('/')
# Create your views here.
