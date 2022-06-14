from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone


    
class BargainItem(models.Model):
    name = models.CharField(max_length=32)
    price = models.IntegerField()
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    profit = models.IntegerField()
    average_price = models.IntegerField()
    sales_rate = models.IntegerField()
    datetime = models.DateTimeField(default=timezone.now)
    category_id = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'bargain_item'
        ordering = ('-datetime',)
