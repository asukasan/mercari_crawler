from django.test import TestCase
from item_management.models import BookCategory, Item, BargainItem


class CategoryModelTests(TestCase):
    
    def test_is_empty(self):
        saved_posts = BookCategory.objects.all()
        self.assertEqual(saved_posts.count(), 0)

    def test_is_count_one(self):
        post = BookCategory.objects.create(name="hogehoge", book_category_id="111")
        post.save()
        saved_posts = BookCategory.objects.all()
        self.assertEqual(saved_posts.count(), 1)

    def test_saving_and_retrieving_post(self):
        category = BookCategory()
        name = "hogehoge"
        book_category_id = "111"
        category.name = name
        category.book_category_id = book_category_id
        category.save()


        saved_category = BookCategory.objects.all()
        actual_category = saved_category[0]

        self.assertEqual(actual_category.name, name)
        self.assertEqual(actual_category.book_category_id, book_category_id)

