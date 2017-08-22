# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

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
		if len(postData['last_name'])<3:
			#print "first_name failed"
			result['errors'].append('Last name should be not fewer than 3 characters')
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
			dob = parser.parse(postData['dob'])
		except (ValueError, MultiValueDictKeyError):
			result['errors'].append("Wrong date format")
			return result
		if relativedelta(datetime.now(), datetime.combine(dob, datetime.min.time())).years < 18:
			result['errors'].append("You have to be at least 18 years old")
		
		if len(result['errors'])>0:
			result['status'] = False
		return result


class Monthes(models.Model):
	name = models.CharField(max_length=255)

class Users(models.Model):
	name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	dob = models.DateField(max_length=8)
	#birthday = models.DateField(null=True, blank=True)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	month = models.ForeignKey(Monthes, related_name="month_at")

	objects = courseManager()





# Create your models here.
