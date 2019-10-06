from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt


app_name = 'exp_service'
urlpatterns = [
    path('', csrf_exempt(views.home), name='home'),
    path('item/<int:item_id>', csrf_exempt(views.item), name='item'),
    path('admin/', admin.site.urls),
]