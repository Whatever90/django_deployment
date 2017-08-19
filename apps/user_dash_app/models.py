# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class courseManager(models.Manager):
	def basic_validator(self, postData):
		#print postData	
		result = {'status': True, 'errors': []}
		if len(postData['first_name'])<3:
			#print "first_name failed"
			result['errors'].append('First name should be not fewer than 3 characters')
		if len(postData['last_name'])<3:
			#print "last name failed"
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
		if len(result['errors'])>0:
			result['status'] = False
		return result

	def login(self,postData):
		print postData
		result = {'status': True, 'errors': []}
		

class Users(models.Model):
 	first_name = models.CharField(max_length=255)
 	last_name = models.CharField(max_length=255)
 	email = models.CharField(max_length=255)
 	password = models.CharField(max_length=255)
 	desc = models.TextField()
 	level = models.IntegerField()
 	created_at = models.DateTimeField(auto_now_add=True)
 	objects = courseManager()

class Posts(models.Model):
	post = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True) 
	postedto = models.ForeignKey(Users, related_name="postedto")
	poster = models.ForeignKey(Users, related_name="poster")
 

class Comments(models.Model):
	comment = models.TextField(max_length=500)
	created_at = models.DateTimeField(auto_now_add=True) 
	poster = models.ForeignKey(Users, related_name="commenter")
	postedto = models.ForeignKey(Posts, related_name="commentedto")

# Create your models here.
