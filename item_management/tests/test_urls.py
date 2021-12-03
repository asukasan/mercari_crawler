from django.test import TestCase
from django.urls import reverse, resolve
from item_management.views import BargainItemTop

class TestUrls(TestCase):
    def test_top_url(self):
        view = resolve('/')
        self.assertEqual(view.func.view_class, BargainItemTop)