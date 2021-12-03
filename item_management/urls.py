from django.urls import path
from .views import BargainItemTop, ItemUpdate, BargainItemScore, crawl_button

app_name = 'item_management'

urlpatterns = [
    path('', BargainItemTop.as_view(), name='home'),
    path('itemupdate/<int:pk>/', ItemUpdate.as_view(), name='item_update'),
    path('bargainscore/<int:score>/', BargainItemScore.as_view(), name='score'),
    path('crawl_button/<int:item_id>/', crawl_button, name='crawl_button'),
]
