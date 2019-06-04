import datetime 
import pytz
from django.test import TestCase

from ..forms import *


class TodoFormTest(TestCase):

	def setUp(self):
		self.t_form=TodoForm(data={'day':'Sunday','activity':'Go swimming'})

	def test_field_label(self):
		self.assertTrue(self.t_form.fields['day'].label == 'Day of the week') # the verbose name or the field name translates to the field label

	def test_todo_form_is_valid(self):
		form=TodoForm(data={'day':'','activit':''})
		self.assertFalse(form.is_valid())

	# def test_character_number(self):
	# 	num_chars=self.t_form.fields['day'].choices.value
	# 	self.assertTrue(len(num_chars)<=15)

	# def test_choice_in_choices(self):
	# 	self.assertIn(self.t_form.fields['day'].value,['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'])


class EmailFormTest(TestCase):

	def setUp(self):
		self.e_form=EmailForm(data={'notify':'','email':'Go swimming','notify_when':datetime.datetime.now(pytz.utc)})


	def test_email_form_is_valid(self):
		self.assertFalse(self.e_form.is_valid())
