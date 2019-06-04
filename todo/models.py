from django.db import models
from django.contrib.auth.models import User
import datetime


class Todo(models.Model):
	DAY_CHOICES=(('Sunday','Sunday'),('Monday','Monday'),('Tuesday','Tuesday'),
		('Wednesday','Wednesday'),('Thursday','Thursday'),('Friday','Friday'),('Saturday','Saturday'))
	author=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	day=models.CharField(max_length=15,choices=DAY_CHOICES,default="Sunday",verbose_name="Day of the week")
	activity=models.TextField()
	date_created=models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.activity


class Email(models.Model):
	to_be_notified=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='to_notify')
	notify=models.TextField()
	email=models.EmailField(max_length=254,blank=False,null=False)
	notify_when=models.DateTimeField(verbose_name="When to notify")

	def __str__(self):
		return self.email

	def notify_(self):
		return self.notify
