# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import EventSub
from .forms import EventSubForm
from django.contrib import messages

def index(request):
	# Initialize form
	form = EventSubForm()

	# When submitting form...	
	if request.method == 'POST':
		form = EventSubForm(request.POST) # fill in the data

		# if data passess validation
		if form.is_valid():
			form.save() # save it!
			messages.success(request, 'Thank you %s, you have successfully registered for the Event!' % (form.cleaned_data['name']))
			return HttpResponseRedirect('/')

	return render(request, 'event_sub/event_sub_form.html', {
		'form': form,
		'event_subs': EventSub.objects.all()[:5],
	})
