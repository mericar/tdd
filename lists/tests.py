#This test suite functions as a part of the project unit tests.

from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpResponse, HttpRequest
from django.template.loader import render_to_string
from lists.models import Item


class HomePageTest(TestCase):

	def test_root_url_resolves_to_homepage(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)
		

class ItemModelTest(TestCase):

	def test_save_retrieve_items(self):
		#make one item
		first = Item()
		first.text = 'first item'
		first.save()

		#make a second item
		second = Item()
		second.text = 'second item'
		second.save()

		#get all of the items
		all_items = Item.objects.all()
		self.assertEqual(all_items.count(), 2)

		#retrieve first and second items
		first_item = all_items[0]
		second_item = all_items[1]
		self.assertEqual(first_item.text, 'first item')
		self.assertEqual(second_item.text, 'second item')

class ListViewTest(TestCase):

	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_all_items(self):
		Item.objects.create(text='itemey 1')
		Item.objects.create(text='itemey 2')
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertContains(response, 'itemey 1') 
		self.assertContains(response, 'itemey 2') 


class NewListTest(TestCase):

	def test_saving_a_POST_request(self):
		self.client.post('/lists/new', data={'item_text': "A new item in the list"})
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item in the list')

	def test_redirects_after_POST(self):
		response = self.client.post('/lists/new', data={'item_text': "A new item in the list"})
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/lists/the-only-list-in-the-world/')





