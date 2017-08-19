# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
class courseManager(models.Manager):
	def basic_validator(self, postData):
		error = ""
		if len(postData['name']) < 5:
			error += "Name should be more than 5 characters  "
		if len(postData['desc']) <15:
			error+= "  Description should be more that 15 characters"
		return error	

class Course(models.Model):
 	name = models.CharField(max_length=255)
 	desc = models.CharField(max_length=255)
 	created_at = models.DateTimeField(auto_now_add=True)
 	updated_at = models.DateTimeField(auto_now=True, null=True)
 	objects = courseManager()

	
	
