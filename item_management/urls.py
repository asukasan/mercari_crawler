from django.urls import path
from .views import BargainItemTop

app_name = 'item_management'

urlpatterns = [
    path('', BargainItemTop.as_view(), name='home'),
]
