# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class courseManager(models.Manager):
	def basic_validator(self, postData):
		error = ""
		if len(postData['first_name']) < 2:
			error += "First name should be more than 5 characters  "
		if len(postData['last_name']) < 2:
			error += "Last name should be more than 5 characters  "	
		if len(postData['email']) < 1:
			error+= "  Email should be more that 15 characters"
		return error	

class User(models.Model):
 	first_name = models.CharField(max_length=255)
 	last_name = models.CharField(max_length=255)
 	email = models.CharField(max_length=255)
 	password = models.CharField(max_length=255)
 	confirm_password = models.CharField(max_length=255)

 	objects = courseManager()
# Create your models here.
