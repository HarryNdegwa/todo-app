import pytz
from datetime import datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import TodoForm,EmailForm
from .models import Todo,Email
from .tasks import send_notification

# @login_required
def home(request):
	todos=Todo.objects.all().order_by('-date_created')
	notifications=Email.objects.values_list('notify',flat=True)
	times=Email.objects.values_list('notify_when',flat=True)
	send_notification.delay()
	print(times)
	if datetime.now(pytz.utc)==datetime(1999, 1, 1, 12, 45, 59):
		print('Helloo world')
	else:
		print(str(times))
		print("heyya world")
	# notificationsv=Email.objects.values('email') # returns a list of dictionaries
	# print(notificationsv[0])
	# print(notifications)
	# print(type(notifications))
	return render(request,'todo/home.html',{'todos':todos,'notifications':notifications})

# @login_required(login_url="login")
@login_required
def create_todo(request):
	if request.method=="POST":
		form=TodoForm(request.POST)
		if form.is_valid():
			my_form=form.save(commit=False)
			my_form.author=request.user
			my_form.save()
			return redirect('home')
	else:
		form=TodoForm()
	return render(request,'todo/todo_create.html',{'form':form})

# @login_required
def edit_todo(request,todo_id):
	todo=Todo.objects.get(id=todo_id)
	todo=get_object_or_404(Todo,pk=todo_id)
	if request.method=="POST":
		form=TodoForm(request.POST,instance=todo)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form=TodoForm(instance=todo)
	return render(request,'todo/edit.html',{'form':form})

# @login_required
def delete_todo(request,todo_id):
	to_delete=Todo.objects.get(id=todo_id)
	to_delete.delete()
	return redirect('home')



def notify_me(request,todo_id):
	data=Todo.objects.get(id=todo_id).activity
	if request.method=="POST":
		form=EmailForm(request.POST)
		if form.is_valid():
			form_instance=form.save(commit=False)
			form_instance.to_be_notified=request.user
			form_instance.save()
			return redirect('home')
	else:
		form=EmailForm(initial={'notify':data})
	return render(request,'todo/notify.html',{'form':form})
