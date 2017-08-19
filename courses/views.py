# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
# the index function is called when root is visited
def register(request):
  response = "placeholder for users to create a new user record"
  return HttpResponse(response)
# Create your views here.
def login(request):
	response = 'placeholder for users to login' 
	return HttpResponse(response)