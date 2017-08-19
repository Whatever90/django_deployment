from __future__ import unicode_literals

from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class courseManager(models.Manager):
	def basic_validator(self, postData):
		#print postData	
		result = {'status': True, 'errors': []}
		if len(postData['name'])<1:
			#print "first_name failed"
			result['errors'].append('Put your name')
		if type(str(postData['name'])) != str:
			#print "first_name failed"
			result['errors'].append('Name shall be a string!')
		if len(postData['age'])<1:
			#print "last name failed"
			result['errors'].append('Put your age')
		if type(int(postData['age'])) != int:
			#print "last name failed"
			result['errors'].append('Age shall be a number!')
		
		#print result['errors']
		if len(result['errors'])>0:
			result['status'] = False
		return result	

class Ages(models.Model):
	age = models.CharField(max_length=255)
	length = models.IntegerField()

class Users(models.Model):
 	name = models.CharField(max_length=255)
 	age = models.IntegerField()
 	age_field = models.ForeignKey(Ages, related_name="aged_to")

 	objects = courseManager()


class Comments(models.Model):
	content = models.CharField(max_length=255)
	poster = models.ForeignKey(Users, related_name="ager")
	posted_to = models.ForeignKey(Ages, related_name="postaged_to")
	created_at = models.DateTimeField(auto_now_add=True)
	