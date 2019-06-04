import pytz
from datetime import datetime
from django .test import TestCase,RequestFactory
from django.shortcuts import reverse
from django.contrib.auth.models import User

from ..views import home,create_todo,delete_todo
from ..models import Todo,Email
from ..forms import EmailForm,TodoForm

class ViewsTestCase(TestCase):


	@classmethod
	def setUpTestData(cls):
		print("Setting up un-modified data")

	def setUp(self):
		# every test needs access to the request factory hence i place it in the setUp block
		# self.factory=RequestFactory() # plays the same role with the client test object
		self.user=User.objects.create_superuser(username='harrison',email='harryndegwa4@gmail.com',password="testuser")
		self.todo=Todo.objects.create(author=self.user,day="Sunday",activity="Sleep the whole day")
		self.email=Email.objects.create(notify="Go to school",
			email="harryndegwa4@gmail.com",notify_when=datetime.now(pytz.utc))
		self.invalid_todo=Todo.objects.create(author=self.user,day="",activity="Sleep the whole day")
		self.invalid_email=Email.objects.create(notify="Go to school",email="",notify_when=datetime.now(pytz.utc))

	def  test_home_view(self):
		r=self.client.get(reverse('home'))
		self.assertEqual(r.status_code,200)
		# self.assertTemplateUsed(r,'todo/home.html')
		self.assertContains(r,'Sleep the whole day')



	def test_create_view(self):
		url=reverse('create')
		resp=self.client.get(url)
		self.assertEqual(resp.status_code,302) # 302 is the status code for http redirects used when we dont know the correct redirect url
		self.assertTrue(resp.url.startswith('/login/')) # we know that the user redirects to the login page bt we dont know the next step

	def test_edit_view(self):
		url=reverse('edit',kwargs={'todo_id':1})
		resp=self.client.get(url)
		self.assertEqual(resp.status_code,200)


	def test_edit_params(self):
		url=reverse('edit',kwargs={"todo_id":1})
		resp=self.client.get(url)
		self.assertEqual(resp.status_code,200)

	def test_delete_todo(self):
		url=reverse('delete',kwargs={'todo_id':1})
		resp=self.client.get(url)
		self.assertEqual(resp.status_code,302)
		# self.assertEqual(resp.target_status_code,200)
		# self.assertTemplateUsed(resp,'todo/home.html') used for views which render

	def test_notify_me(self):
		url=reverse('notify_me',kwargs={'todo_id':1})
		resp=self.client.get(url)
		self.assertEqual(resp.status_code,200)


	def test_invalid_id(self):
		url=reverse('notify_me',kwargs={'todo_id':str(1)})
		resp=self.client.get(url)
		self.assertEqual(resp.status_code,200)


	def test_valid_email_form(self):
		data=self.email
		form=EmailForm(data={'notify':data.notify,'email':data.email,'notify_when':data.notify_when})
		self.assertTrue(form.is_valid())


	def test_invalid_email_form(self):
		data=self.invalid_email
		form=EmailForm(data={'notify':data.notify,'email':data.email,'notify_when':data.notify_when})
		self.assertFalse(form.is_valid())


	def test_valid_todo_form(self):
		data=self.todo
		form=TodoForm(data={'author':self.user,'day':data.day,'activity':data.activity})
		self.assertTrue(form.is_valid())


	def test_invalid_todo_form(self):
		data=self.invalid_todo
		form=TodoForm(data={'day':data.day,'activity':data.activity})
		self.assertFalse(form.is_valid())

	def test_todo_email_data(self):
		url=reverse('notify_me',kwargs={'todo_id':1})
		resp=self.client.post(url,data={'notify':self.email.notify,'email':self.email.email,'notify_when':self.email.notify_when})
		self.assertEqual(resp.status_code,200)


	def test_todo_edit_data(self):
		url=reverse('edit',kwargs={'todo_id':1})
		resp=self.client.post(url,data={'notify':self.email.notify,'email':self.email.email,'notify_when':self.email.notify_when})
		self.assertEqual(resp.status_code,200)


	def test_todo_data(self):
		url=reverse('create')
		self.client.login(username=self.user.username,password=self.user.password)
		resp=self.client.post(url,data={'author':self.user,'day':self.todo.day,'activity':self.todo.activity})
		self.assertEqual(resp.status_code,302)


	def test_view_url_accessed_by_name(self):
		url=reverse('home')
		resp=self.client.get(url)
		self.assertEqual(resp.status_code,200)

	def test_create_view_redirects_correctly(self):
		response=self.client.get(reverse('create'))
		# self.assertRedirects(response,'login')
		self.assertRedirects(response,'/login/?next=/create/') # we use assertRedirects here because we know the redirect utl

	def test_user_is_logged_in(self):
		login=self.client.login(username='harrison',password='testuser') # use actual values, not object references
		url=reverse('create')
		resp=self.client.get(url)
		self.assertEqual(str(resp.context['user']),'harrison')


	def test_user_is_logged_out(self):
		logout=self.client.logout()
		resp=self.client.get('logout')
		# self.assertRedirects(resp,'/login/')
		self.assertEqual(resp.status_code,404)
		# self.assertEqual(str(resp.context['user'],''))
		self.assertFalse('user' in resp.context) # there is no user object after logging out.

