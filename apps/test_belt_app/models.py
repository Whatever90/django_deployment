from __future__ import unicode_literals

from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class courseManager(models.Manager):
	def basic_validator(self, postData):
		result = {'status': True, 'errors': []}
		if len(postData['name'])<3:
			#print "first_name failed"
			result['errors'].append('Name should be not fewer than 3 characters')
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



class Users(models.Model):
 	name = models.CharField(max_length=255)
 	email = models.CharField(max_length=255)
 	password = models.CharField(max_length=255)
 	gold = models.IntegerField()
 	activities = models.TextField()
 	created_at = models.DateTimeField(auto_now_add=True)

 	objects = courseManager()


class Logs(models.Model):
	content = models.TextField()
	us = models.ForeignKey(Users, related_name="poster")
	created_at = models.DateTimeField(auto_now_add=True)
	