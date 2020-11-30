from django.shortcuts import render
from products.models import Product
# Create your views here.


def index(request):
    """view to return index html"""
    season = Product.objects.filter(seasonal=True)
    template = 'home/index.html'
    context = {'season': season}
    return render(request, template, context)
