from .custom_date import get_custom_date
# from .django_model_setup import d_setup
# d_setup(db_name="mercari_db")
from item_management.models import BargainItem

def bargain_item_delete(custom_date=1):
    custom_date = get_custom_date(days=custom_date)
    BargainItem.objects.filter(datetime__lt=custom_date).delete()