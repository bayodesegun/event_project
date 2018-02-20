from django.forms import ModelForm
from .models import EventSub

class EventSubForm(ModelForm):
	class Meta:
		model = EventSub
		fields = ('name', 'email', )