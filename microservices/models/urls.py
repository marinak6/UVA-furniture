from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

app_name = 'models'
urlpatterns = [
    path('bid/create/', views.createBid, name='create-bid'),
    path('furniture/create/', csrf_exempt(views.createFurniture),
         name='createFurniture'),

]
