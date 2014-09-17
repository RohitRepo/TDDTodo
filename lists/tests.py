from django.test import TestCase
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from lists.views import home_page
from lists.models import Item

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
	found = resolve('/')
	self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
	request = HttpRequest()
	response = home_page(request)
	expected_html = render_to_string('home.html')
	self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_saves_only_when_necessary(self):
	request = HttpRequest()
	response = home_page(request)
	self.assertEqual(Item.objects.count(), 0)


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
	first_item_text = 'A new list'
	response = self.client.post('/lists/new',
		data={'item_text': first_item_text}
	)

	self.assertEqual(Item.objects.count(), 1)
	first_saved_item = Item.objects.first()
	self.assertEqual(first_saved_item.text, first_item_text)

    def test_redirect_after_POST(self):
	first_item_text = 'A new list'
	response = self.client.post('/lists/new',
		data={'item_text': first_item_text}
	)

	self.assertRedirects(response, '/lists/the-only-list/')

class ListViewTest(TestCase):

    def test_view_page_displays_all_items(self):
	first_item = Item.objects.create(text = "Item1")
	second_item = Item.objects.create(text = "Item2")

	response = self.client.get('/lists/the-only-list/')

	self.assertContains(response, 'Item1')
	self.assertContains(response, 'Item2')

    def test_uses_list_template(self):
	response = self.client.get('/lists/the-only-list/')
	self.assertTemplateUsed(response, 'list.html')

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
	first_item = Item()
	first_item.text = 'The firs list item'
	first_item.save()

	second_item = Item()
	second_item.text = 'The second list item'
	second_item.save()

	saved_items = Item.objects.all()
	self.assertEqual(saved_items.count(), 2)

	first_saved_item = saved_items[0]
	second_saved_item = saved_items[1]
	self.assertEqual(first_saved_item.text, first_item.text)
	self.assertEqual(second_saved_item.text, second_item.text)
