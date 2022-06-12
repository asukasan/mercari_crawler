from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone


class BookCategory(models.Model):
    name = models.CharField(max_length=32)
    book_category_id = models.CharField(max_length=32)

    def __str__(self):
        return self.name 
    
class BargainItem(models.Model):
    name = models.CharField(max_length=32)
    price = models.IntegerField()
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    profit = models.IntegerField()
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'bargain_item'
        ordering = ('-datetime',)
