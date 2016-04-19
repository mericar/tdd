#This test suite functions as a part of the project unit tests.

from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpResponse, HttpRequest
from django.template.loader import render_to_string


class HomePageTest(TestCase):

	def test_root_url_resolves_to_homepage(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)

	def test_homepage_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new item in the list'

		response = home_page(request)

		self.assertIn('A new item in the list', response.content.decode())
		expected_html =render_to_string('home.html', {'new_item_text':'A new item in the list'})



