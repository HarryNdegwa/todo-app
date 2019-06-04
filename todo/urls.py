from django.urls import path

from . import views


urlpatterns=[
	path('home/',views.home,name='home'),
	path('create/',views.create_todo,name='create'),
	path('edit/<int:todo_id>/',views.edit_todo,name='edit'),
	path('delete/<int:todo_id>/',views.delete_todo,name='delete'),
	path('notify/<int:todo_id>/',views.notify_me,name='notify_me'),
]