from django.test import TestCase
from django.core.exceptions import ValidationError

from event_sub.forms import EventSubForm

class EventSubFormTest(TestCase):
	def test_valid_form_data(self):
	    form = EventSubForm({
	        'name': "John Doe",
	        'email': "john.doe@example.com",
	    })
	    self.assertTrue(form.is_valid())
	    sub = form.save()
	    self.assertEqual(sub.name, "John Doe")
	    self.assertEqual(sub.email, "john.doe@example.com")

	def test_blank_data_invalidates_form(self):
	    form = EventSubForm({})
	    self.assertFalse(form.is_valid())
	    self.assertEqual(form.errors, {
	        'name': ['This field is required.'],
	        'email': ['This field is required.'],
	    })

	def test_invalid_email_is_not_accepted(self):
	    form = EventSubForm({
	        'name': "John Doe",
	        'email': "john.doe@example",
	    })
	    self.assertFalse(form.is_valid())
	    self.assertEqual(form.errors, {
	        'email': ['Enter a valid email address.'],
	    })

	def test_email_cannot_be_registered_twice(self):
	    form = EventSubForm({
	        'name': "John Doe",
	        'email': "john.doe@example.com",
	    })
	    form.save()

	    form2 = EventSubForm({
	        'name': "John Doe 2",
	        'email': "john.doe@example.com",
	    })
	    self.assertFalse(form2.is_valid())
	    self.assertEqual(form2.errors, {
	        'email': ['Event sub with this Email already exists.'],
	    })