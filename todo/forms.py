from django import forms
# from bootstrap_datepicker_plus import DateTimePickerInput

from .models import Todo,Email


class TodoForm(forms.ModelForm):
	class Meta:
		model=Todo
		fields=['day','activity']


class EmailForm(forms.ModelForm):
	notify_when=forms.DateTimeField(input_formats=('%d-%m-%Y %H:%M:%S',))
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['notify'].widget.attrs['label']='To notify'
		self.fields['notify_when'].widget.attrs['placeholder']='d-m-Y H:M:S eg1-1-1999 12:45:59'

	class Meta:
		model=Email
		exclude=['to_be_notified',]
