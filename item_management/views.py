from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from .models import BargainItem
from django.http import HttpResponseRedirect


class BargainItemTop(TemplateView):

    template_name = "item_management/bargain_item.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bargain_items'] = BargainItem.objects.all()[:10]
        return context
