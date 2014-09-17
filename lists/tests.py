from django.test import TestCase
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from lists.views import home_page
from lists.models import Item, List

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
	found = resolve('/')
	self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
	request = HttpRequest()
	response = home_page(request)
	expected_html = render_to_string('home.html')
	self.assertEqual(response.content.decode(), expected_html)


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

	new_list = List.objects.first()
	self.assertRedirects(response, '/lists/%d/' %(new_list.id,))

class ListViewTest(TestCase):

    def test_view_page_displays_all_items_of_one_list(self):
	correct_list = List.objects.create()
	correct_first_item = Item.objects.create(text = "Item1", list=correct_list)
	correct_second_item = Item.objects.create(text = "Item2", list=correct_list)

	wrong_list = List.objects.create()
	wrong_first_item = Item.objects.create(text="wrong item1", list = wrong_list)
	wrong_first_item = Item.objects.create(text="wrong item2", list = wrong_list)

	response = self.client.get('/lists/%d/' %(correct_list.id,))

	self.assertContains(response, 'Item1')
	self.assertContains(response, 'Item2')
	self.assertNotContains(response, 'wrong item1')
	self.assertNotContains(response, 'wrong item2')

    def test_uses_list_template(self):
	item_list = List.objects.create()
	response = self.client.get('/lists/%d/' %(item_list.id))
	self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
	wrong_list = List.objects.create()
	correct_list = List.objects.create()

	response = self.client.get('/lists/%d/' %(correct_list.id,))
	self.assertEqual(response.context['list'], correct_list)

class AddItemTest(TestCase):

    def test_add_new_item_on_POST(self):
	item_list = List.objects.create()
	dummy_item_list = List.objects.create()
	response = self.client.post('/lists/%d/add-item' %(item_list.id, ),
		data = {'item_text': 'item to existing list'}
	)

	self.assertEqual(Item.objects.count(), 1)
	new_item = Item.objects.first()
	self.assertEqual(new_item.text, "item to existing list")
	self.assertEqual(new_item.list, item_list)
	self.assertEqual(dummy_item_list.item_set.count(), 0)

    def test_redirect_after_POST(self):
	item_list = List.objects.create()
	response = self.client.post('/lists/%d/add-item' %(item_list.id, ),
		data = {'item_text': 'item to existing list'}
	)

	self.assertRedirects(response, '/lists/%d/' %(item_list.id,))


class ItemAndListModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
	first_list = List()
	first_list.save()

	first_item = Item()
	first_item.text = 'The firs list item'
	first_item.list = first_list
	first_item.save()

	second_item = Item()
	second_item.text = 'The second list item'
	second_item.list = first_list
	second_item.save()

	saved_items = Item.objects.all()
	self.assertEqual(saved_items.count(), 2)

	first_saved_item = saved_items[0]
	second_saved_item = saved_items[1]
	self.assertEqual(first_saved_item.text, first_item.text)
	self.assertEqual(first_saved_item.list, first_list)
	self.assertEqual(second_saved_item.text, second_item.text)
	self.assertEqual(second_saved_item.list, first_list)
