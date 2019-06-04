import pytz
from datetime import datetime
from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User

from ..models import Todo,Email
from ..views import home,create_todo,delete_todo


class Todo_TestCase(TestCase):

	def setUp(self):
		self.user=User.objects.create(username='harrison')
		self.todo=Todo.objects.create(author=self.user,day="Sunday",activity="Start a gis web application")
		self.email=Email.objects.create(notify='go to school',
			email='harryndegwa4@gmail.com',notify_when=datetime.now(pytz.utc))

	def test_todo_creation(self):
		todo=self.todo
		self.assertIsInstance(todo,Todo)
		self.assertEqual(todo.activity,"Start a gis web application")
		self.assertEqual(todo.__str__(),todo.activity)

	def test_create_email(self):
		self.assertIsInstance(self.email,Email)
		self.assertEqual(self.email.__str__(),self.email.email)
		self.assertEqual(str(self.email),self.email.email)


	def test_notify(self):
		self.assertEqual(self.email.notify,self.email.notify_())

	def test_valid_field(self):
		self.assertTrue(len(self.todo.day)<=15)

	def test_not_null(self):
		self.assertTrue(self.todo.day != '')

	def test_field_label(self):
		field_label=self.todo._meta.get_field('day').verbose_name
		max_length=self.todo._meta.get_field('day').max_length
		self.assertTrue(15==max_length)
		self.assertEqual(field_label,'Day of the week')


	def test_null_is_true(self):
		nullable=self.todo._meta.get_field('author').null
		self.assertTrue(nullable)