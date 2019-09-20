from django.contrib import admin

# Register your models here.
from .models import Bid, Person, Category, Furniture

admin.site.register(Bid)
admin.site.register(Person)
admin.site.register(Category)
admin.site.register(Furniture)
