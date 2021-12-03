from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone

from crawler.mercari_driver import custom_time_sleep

class BookCategory(models.Model):
    name = models.CharField(max_length=32)
    book_category_id = models.CharField(max_length=32)

    def __str__(self):
        return self.name 
    


class Item(models.Model):
    name = models.CharField(max_length=124, unique=True)
    item_quantity = models.IntegerField()
    average_price = models.IntegerField()
    sales_rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    crawl = models.BooleanField(default=True)
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE)
    last_updated = models.DateField(default=timezone.now)

    def switch(self):
        if self.crawl:
            self.crawl = False
            self.save()
        else:
            self.crawl = True    
            self.save()

    class Meta:
        db_table = 'item'

    def __str__(self):
        return self.name

class BargainItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.IntegerField()
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    profit = models.IntegerField()
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.item.name

    class Meta:
        db_table = 'bargain_item'
        ordering = ('-datetime',)
