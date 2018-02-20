from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import CharField, EmailField

from event_sub.models import EventSub

class EventSubModelTest(TestCase):
	""" This class defines the test suite for the EventSub model """	
	def setUp(self):
		# runs before all test methods, with clean data
		self.sub = EventSub.objects.create()

	def test_name_field_exists_with_correct_max_length(self):
		field = self.sub._meta.get_field('name')
		self.assertEquals(field.max_length, 50)

	def test_name_field_exists_with_correct_field_type(self):
		field = self.sub._meta.get_field('name')
		self.assertTrue(isinstance(field, CharField))

	def test_name_field_exists_with_correct_label(self):
		field = self.sub._meta.get_field('name')
		self.assertEquals(field.verbose_name, 'name')

	def test_name_field_exists_with_correct_help_text(self):
		field = self.sub._meta.get_field('name')
		self.assertEquals(field.help_text, 'Please enter your name')

	def test_email_field_exists_with_correct_field_type(self):
		field = self.sub._meta.get_field('email')
		self.assertTrue(isinstance(field, EmailField))

	def test_email_field_exists_with_correct_label(self):
		field = self.sub._meta.get_field('email')
		self.assertEquals(field.verbose_name, 'email')

	def test_email_field_exists_with_correct_help_text(self):
		field = self.sub._meta.get_field('email')
		self.assertEquals(field.help_text, 'Please enter your email')

	def test_name_is_required(self):
		self.sub.name = 'nerd@example.com'
		with self.assertRaises(ValidationError):
			self.sub.save()
			self.sub.full_clean()

	def test_email_is_required(self):
		self.sub.name = 'Nerd'
		with self.assertRaises(ValidationError):
			self.sub.save()
			self.sub.full_clean()

	def test_model_string_representation_is_correct(self):
		self.sub.name = 'Nerd'
		self.sub.email = 'nerd@example.com'
		self.sub.save()
		self.assertEquals(str(self.sub), 'Nerd - nerd@example.com')

	def test_model_email_field_is_unique(self):
		self.sub.name = 'Nerd'
		self.sub.email = 'nerd@example.com'
		self.sub.save()

		with self.assertRaises(IntegrityError):
			sub2 = EventSub.objects.create(name='Nerd 2', email='nerd@example.com')
			sub2.save()
