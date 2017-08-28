# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.utils.datastructures import MultiValueDictKeyError
from dateutil.relativedelta import relativedelta
from dateutil import parser
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class courseManager(models.Manager):
	def basic_validator(self, postData):
		result = {'status': True, 'errors': []}
		if len(postData['name'])<3:
			#print "first_name failed"
			result['errors'].append('Name should be not fewer than 3 characters')
		if not postData['name'].isalpha():
			result['errors'].append('Name should have letters, not numbers')
		if len(postData['alias'])<1:
			#print "first_name failed"
			result['errors'].append('Alias should be not fewer than 1 characters')
		if not EMAIL_REGEX.match(postData['email']):
			#print "email failed"
			result['errors'].append('Email should be right format')
		if len(postData['password'])<8:
			#print "pw longth failed"
			result['errors'].append('Password should be not fewer than 8 characters')
		if postData['password'] != postData['confirm']:
			#print "pw and cpw don't match"
			result['errors'].append("Password don't match")
		#print result['errors']
		try:
			try: 
				dob = parser.parse(postData['dob'])
			except:
				result['errors'].append("Wrong date format")
				return result
		except (ValueError, MultiValueDictKeyError):
			result['errors'].append("Wrong date format")
			return result
		#if relativedelta(datetime.now(), datetime.combine(dob, datetime.min.time())).years < 14:
			#result['errors'].append("You have to be at least 14 years old")
		
		if len(result['errors'])>0:
			result['status'] = False
		return result




class Users(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	dob = models.DateField(max_length=8)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	friends = models.ManyToManyField('self')

	

	objects = courseManager()

class Friends(models.Model):
	
	add_by = models.ManyToManyField(Users, related_name="add")
	add_by = models.ForeignKey(Users, related_name="addby")
	#added = models.ForeignKey(Users, related_name="add")
	#models.ManyToManyField(Publication)
	



# Create your models here.
