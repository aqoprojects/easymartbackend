from django.contrib import admin
from .models import Category, Product, ProductImages, ProductTags, ProductTagAssociations

admin.site.register([Category, Product, ProductImages, ProductTags, ProductTagAssociations])