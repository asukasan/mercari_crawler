from django.shortcuts import redirect, render
from django.views.generic import TemplateView, UpdateView, ListView
from .models import BargainItem, Item
from .forms import ItemUpdateForm
from django.http import HttpResponseRedirect


class BargainItemTop(TemplateView):

    template_name = "item_management/bargain_item.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bargain_items'] = BargainItem.objects.all()[:10]
        return context


class ItemUpdate(UpdateView):
    template_name = "item_management/item_update.html"
    model = Item
    form_class = ItemUpdateForm
    success_url = "/"


class BargainItemScore(ListView):
    template_name = "item_management/bargain_item_score.html"
    model = BargainItem
    context_object_name = 'items'

    def get_queryset(self):
        score = self.kwargs['score']
        items = self.model.objects.filter(score=score)[:10]
        return items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['score'] = self.kwargs['score']
        return context
        
def crawl_button(request, item_id):
    if request.method == "POST":
        item = Item.objects.get(id=item_id)
        item.switch()
    return HttpResponseRedirect("/")