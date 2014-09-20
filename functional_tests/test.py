import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
	for arg in sys.argv:
	    if 'liveserver' in arg:
		cls.server_url = 'http://' + arg.split('=')[1]
		return

	super(NewVisitorTest, cls).setUpClass()
	cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
	if cls.server_url == cls.live_server_url:
	   super(NewVisitorTest, cls).tearDownClass()


    def setUp(self):
	self.browser = webdriver.Firefox()
	self.browser.implicitly_wait(3)

    def tearDown(self):
	self.browser.quit()

    def check_for_row_in_table(self, row_text):
	table = self.browser.find_element_by_id('id_list_table')
	rows = table.find_elements_by_tag_name('tr')
	self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
	# Tesla goes to check out the home page
	self.browser.get(self.server_url)
	
	# He notices the title mentions To-Do
	self.assertIn('To-Do', self.browser.title)
	header_text = self.browser.find_element_by_tag_name('h1').text
	self.assertIn('To-Do', header_text)
	
	# He is invited to enter a ToDo item straight away.
	input_box = self.browser.find_element_by_id('id_new_item')
	self.assertEqual(
		input_box.get_attribute('placeholder'),
		'Enter a to-do item'
	)

	# He types 'Call Faraday' into text box
	first_list_item = 'Call Faraday'
	input_box.send_keys(first_list_item)

	# When he hits enter, he is taken to a new page, and now
	# lists '1: Call Faraday' as an item in a to-do list
	input_box.send_keys(Keys.ENTER)
	tesla_list_url = self.browser.current_url
	self.assertRegexpMatches(tesla_list_url, '/lists/.+')

	self.check_for_row_in_table('1: ' + first_list_item)
	# There is still a test-box inviting him to enter
	# another item. He enters "Use that information" as an item to ToDo list
	input_box = self.browser.find_element_by_id('id_new_item')
	second_list_item = 'Use that information'
	input_box.send_keys(second_list_item);
	input_box.send_keys(Keys.ENTER)
	
	# Page updates again and shows both the item in his ToDo list
	self.check_for_row_in_table('1: ' + first_list_item)
	self.check_for_row_in_table('2: ' + second_list_item)
	
	# A new user, Newton, comes along to the site.
	##Using a new browser session to ensure Tesla's
	## information is not coming through cookies.

	self.browser.quit()
	self.browser = webdriver.Firefox()

	# Newton visits home page, there is no sign of 
	# Tesla's list
	self.browser.get(self.server_url)
	page_text = self.browser.find_element_by_tag_name('body').text
	self.assertNotIn(first_list_item, page_text)
	self.assertNotIn(second_list_item, page_text)

	# Newton starts a new list by entering new item.
	input_box = self.browser.find_element_by_id('id_new_item')
	newton_first_list_element = 'Buy appples'
	input_box.send_keys(newton_first_list_element)
	input_box.send_keys(Keys.ENTER)

	# Newton gets his own Url.
	newton_list_url = self.browser.current_url
	self.assertRegexpMatches(newton_list_url, '/lists/.+')
	self.assertNotEqual(newton_list_url, tesla_list_url)

	# Again no trace of Tesla
	page_text = self.browser.find_element_by_tag_name('body').text
	self.assertNotIn(first_list_item, page_text)
	self.assertNotIn(second_list_item, page_text)

	# Satisfied he goes to sleep for the day.

    def test_layout_and_styling(self):
	# Tesla goes to home page.
	self.browser.get(self.server_url)
	self.browser.set_window_size(1024, 768)

	# He notices input box nicely centered.
	input_box = self.browser.find_element_by_id('id_new_item')
	self.assertAlmostEqual(input_box.location['x']+input_box.size['width'] / 2,
		512,
		delta=5
	)

	input_box.send_keys(Keys.ENTER)
	input_box = self.browser.find_element_by_id('id_new_item')
	self.assertAlmostEqual(input_box.location['x']+input_box.size['width'] / 2,
		512,
		delta=5
	)

