from django.test import TestCase

# Create your tests here.
from event_sub.models import EventSub
from event_sub.forms import EventSubForm
from django.urls import reverse

class EventSubIndexTest(TestCase):
	""" This class defines the test suite for the event_sub index View """
	@classmethod
	def setUpTestData(cls):
		#Create 7 Event subs for test
		number_of_subs = 7
		for sub_num in range(number_of_subs):
			EventSub.objects.create(name='User %s' % sub_num, email = 'user%s@example.com' % sub_num,)

	def test_view_url_exists_at_desired_location(self): 
		resp = self.client.get('/') 
		self.assertEqual(resp.status_code, 200)  
		   
	def test_view_url_accessible_by_name(self):
		resp = self.client.get(reverse('sub_index'))
		self.assertEqual(resp.status_code, 200)
		
	def test_view_uses_correct_template(self):
		resp = self.client.get(reverse('sub_index'))
		self.assertEqual(resp.status_code, 200)

		self.assertTemplateUsed(resp, 'event_sub/event_sub_form.html')
		
	def test_last_five_registrations_context_variable_is_present_with_correct_size(self):
		resp = self.client.get(reverse('sub_index'))
		self.assertEqual(resp.status_code, 200)
		self.assertTrue( len(resp.context['event_subs']) == 5)

	def test_last_five_registrations_context_variable_is_present_with_correct_data(self):
		resp = self.client.get(reverse('sub_index'))
		self.assertEqual(resp.status_code, 200)
		event_subs = EventSub.objects.all()[:5]
		self.assertEqual(list(resp.context['event_subs']), list(event_subs))

	def test_last_five_registrations_is_present_on_page_in_a_table(self):
		resp = self.client.get(reverse('sub_index'))
		self.assertEqual(resp.status_code, 200)
		event_subs = EventSub.objects.all()[:5]
		self.assertIn('<th>Name</th>', resp.content)
		self.assertIn('<th>Email</th>', resp.content)
		self.assertIn('<th>Subscribed At</th>', resp.content)
		for sub in event_subs:
			self.assertIn('<td>%s</td>' % (sub.name), resp.content)
			self.assertIn('<td>%s</td>' % (sub.email), resp.content)	

	def test_event_sub_empty_form_is_present_on_page(self):
		resp = self.client.get(reverse('sub_index'))
		self.assertEqual(resp.status_code, 200)
		self.assertTrue(isinstance(resp.context['form'], EventSubForm))

	def test_event_sub_empty_form_context_variable_is_present_on_page(self):
		resp = self.client.get(reverse('sub_index'))
		self.assertEqual(resp.status_code, 200)
		form = resp.context['form']
		self.assertIn('<form', resp.content)
		self.assertIn('<input type="text"', resp.content)
		self.assertIn('<input type="email"', resp.content)
		self.assertIn('name="name"', resp.content)
		self.assertIn('name="email"', resp.content)
		self.assertIn('<input type="submit"', resp.content)

	def test_page_should_redirect_after_successful_form_submission(self):
		self.client.get(reverse('sub_index')) # visit the page first
		resp = self.client.post(reverse('sub_index'), {'name': 'Bayode', 'email': 'bayode@bayode.com'})
		self.assertEqual(resp.status_code, 302)
		self.assertRedirects(resp, '/')

	def test_page_should_show_error_on_invalid_form_data_post(self):
		self.client.get(reverse('sub_index')) # visit the page first
		resp = self.client.post(reverse('sub_index'), {'name': 'Bayode', 'email': 'bayode@bayode'})
		self.assertFormError(resp, 'form', 'email', 'Enter a valid email address.')

	def test_page_should_show_error_on_attempt_to_submit_existing_email(self):
		self.client.get(reverse('sub_index')) # visit the page first
		# first save with a given email
		resp = self.client.post(reverse('sub_index'), {'name': 'Bayode', 'email': 'bayode@bayode.com'})
		# then try saving with the same email again
		resp2 = self.client.post(reverse('sub_index'), {'name': 'Kayode', 'email': 'bayode@bayode.com'})
		self.assertFormError(resp2, 'form', 'email', 'Event sub with this Email already exists.')
