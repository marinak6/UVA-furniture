from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt


app_name = 'exp_service'
urlpatterns = [
    path('', csrf_exempt(views.home), name='home'),
    path('item/<int:item_id>', csrf_exempt(views.item), name='item'),
    path('furniture/create', csrf_exempt(views.createFurniture),
         name='createFurniture'),
    path('admin/', admin.site.urls),

    # Authentication
    path('register', csrf_exempt(views.register), name='register'),
    path('login', csrf_exempt(views.login), name='login'),
    path('logout/', csrf_exempt(views.logout), name='logout'),
]
