# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime, date
from django.utils.datastructures import MultiValueDictKeyError
from dateutil.relativedelta import relativedelta
from dateutil import parser
import datetime
import dateutil.parser
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
		if len(postData['alias'])<3:
			#print "first_name failed"
			result['errors'].append('Alias should be not fewer than 3 characters')
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
		#try:
		#	try: 
		#		dob = parser.parse(postData['dob'])
		#	except:
		#		result['errors'].append("Wrong date format")
		#		return result
		#except (ValueError, MultiValueDictKeyError):
		#	result['errors'].append("Wrong date format")
		#	return result
		#if relativedelta(datetime.now(), datetime.combine(dob, datetime.min.time())).years < 14:
			#result['errors'].append("You have to be at least 14 years old")
		
		if len(result['errors'])>0:
			result['status'] = False
		return result

class TripManager(models.Manager):
	def tripvalidator(self, postData):
		result = {'status': True, 'errors': []}
		if len(postData['dest'])<1:
			#print "first_name failed"
			result['errors'].append('Destination should not be empty')
		if not postData['dest'].isalpha():
			result['errors'].append('Destination should have letters, not numbers')
		try:
			try: 
				datefrom = parser.parse(postData['datefrom'])
				dateto = parser.parse(postData['dateto'])
			except:
				result['errors'].append("Wrong date format")
				return result
		except (ValueError, MultiValueDictKeyError):
			result['errors'].append("Wrong date format")
			return result
		print "+++++++++----------------"
		print datefrom.month
		print "CHECKIG!"
		#print ((date.today().year * 365) + (date.today().month * 365))
		d0 = datefrom
		d1 = dateto
		delta = d1 - d0
		print delta.days
		print type(datefrom)
		print type(delta)
		#print int(delta)
		print date.today()
		parsed1 = dateutil.parser.parse(str(d1))
		print parsed1
		a = datetime.datetime(d0.year, d0.month, d0.day)
		print d0.date()
		print d1.date()
		print d0.date() < d1.date()
		print "+++++++++++++++++++------"
		if d0.date() < date.today():
			result['errors'].append("You can't travel back in time")
		if delta.days<0:
			result['errors'].append("You can't travel back in time")
		if len(result['errors'])>0:
			result['status'] = False
		return result


class Users(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	#dob = models.DateField(max_length=8)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	#friends = models.ManyToManyField('self')

	

	objects = courseManager()

class Trips(models.Model):
	destination = models.CharField(max_length=255)
	desc = models.TextField(max_length=1000)
	planned_by = models.ForeignKey(Users, related_name="planner")
	datefrom = models.DateField(max_length=8)
	dateto = models.DateField(max_length=8)
	user = models.ManyToManyField(Users, related_name="joiner")
	created_at = models.DateTimeField(auto_now_add=True)
	#added = models.ForeignKey(Users, related_name="add")
	#models.ManyToManyField(Publication)
	objects = TripManager()



# Create your models here.
