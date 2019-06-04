from __future__ import absolute_import,unicode_literals
from django.core.mail import send_mail
from celery import shared_task



from todoproject.celery import app


# by default the manager for backward access is the name of the model_set
# this one is a registered task
@app.task(bind=True)
def send_todo_notification_email(self):
	recipient_list=['harryndegwa4@gmail.com']
	try:
		send_mail(
				'Your Todo Activity',
				'Remember your todos',
				None,
				recipient_list,
				fail_silently=False,
	    )
	except Exception as e:
		raise self.retry(exc=e)

# this is a shared task
@shared_task 
def send_notification():
     print("Helloo world")
     # Another trick
				