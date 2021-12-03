from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.urls.base import reverse
from item_management.models import BookCategory, Item, BargainItem

class IndexView(TestCase):
    def test_get(self):
        response = self.client.get(reverse('item_management:home'))
        self.assertEqual(response.status_code, 200)

class ItemListTest(TestCase):

    def setUp(self):
        category1 = BookCategory.objects.create(name="コンピュータ/IT", book_category_id="674")
        item1 = Item.objects.create(
            name = "title1",
            item_quantity = 333,
            average_price = 300,
            sales_rate = 89,
            crawl = True,
            category = category1
        )
        bargainitem1 = BargainItem.objects.create(
            item = item1,
            price = 800,
            score = 8,
            profit = 800,
        )

    def test_get(self):
        response = self.client.get(reverse('item_management:home'))
        self.assertEqual(response.status_code, 200)

    def test_get_2item_by_list(self):
        response = self.client.get(reverse('item_management:home'))
        self.assertEqual(response.status_code, 200)
        print(response.context['bargain_items'])
        self.assertQuerysetEqual(
            response.context['bargain_items'],
            ['<BargainItem: title1>'],
            ordered = False
        )
        self.assertContains(response, 'title1')

    def tearDown(self):
        pass