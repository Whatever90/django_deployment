# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.shortcuts import render, redirect
import bcrypt
import re
from django.contrib import messages
from django.core.urlresolvers import reverse
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
	print "we are in the main page"
	return render(request, "age_app/index.html")
# Create your views here.
def registration(request):
	#errors = User.objects.basic_validator(request.POST)
	request.session['err'] = ''
	request.session['error'] = ""
	print request.POST['name']
	print type(str(request.POST['age']))
	results = Users.objects.basic_validator(request.POST)
	if results['status'] == False:
		for error in results['errors']:
			messages.error(request, error)
		return redirect('/')
	
	else:
		print "everything is alright"
		if int(request.POST['age']) <= 10:
			age = Ages.objects.get(id=1)
		if int(request.POST['age']) > 10 and int(request.POST['age']) <=18:
			age = Ages.objects.get(id=2)
		if int(request.POST['age']) > 18 and int(request.POST['age']) <=25:
			age = Ages.objects.get(id=3)
		if int(request.POST['age']) > 25 and int(request.POST['age']) <=35:
			age = Ages.objects.get(id=4)
		if int(request.POST['age']) > 35 and int(request.POST['age']) <=50:
			age = Ages.objects.get(id=5)
		if int(request.POST['age']) > 50:
			age = Ages.objects.get(id=6)

		create = Users.objects.create(name=request.POST['name'], age=request.POST['age'], age_field = Ages.objects.get(id=age.id))
		create.save()
		num = age.length + 1
		age.length = num
		age.save()
		request.session['user'] = {
			'name': request.POST['name'],
			'age': request.POST['age'],
			'id': create.id,
			'group': age.id
		}
		print request.session['user']
		print request.session['user']['age']
		
		return redirect('/dashboard')
	#print "created a new course"
	return redirect('/')

def dashboard(request):
	print 'we r in dashboard'
	context = {
		'ages' : Ages.objects.all().order_by('-length')[:3]
	}
	return render(request, "age_app/index2.html", context)

def specage(request, num):
	a = Ages.objects.get(id=num)
	context = {
		"age": a
	}
	return render(request, "age_app/specage.html", context)

def logout(request):
	request.session['user'].clear()
	return redirect('/')
def message(request):
	a = Comments.objects.create(content=request.POST['message'], poster=Users.objects.get(id=request.POST['user']), posted_to=Ages.objects.get(id=request.POST['group']))
	return redirect(reverse('specage', kwargs={'num':request.session['user']['group']}))
