from django.db import models

# Create your models here.

class Category (models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    name: models.CharField(max_length=254)
    price: models.DecimalField(max_digits=6, decimal_places=2)
    qty: models.CharField(max_length=254)
    description: models.CharField(max_length=254)
    image_url: models.URLField(max_length=1024, blank=True)
    image: models.ImageField(blank=True)

    def __str__(self):
        return self.name
