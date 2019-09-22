from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

app_name = 'models'
urlpatterns = [
    path('bid/create/', views.createBid, name='create-bid'),
    path('furniture/create/', csrf_exempt(views.createFurniture),
         name='createFurniture'),
    path('furniture/<int:id>', csrf_exempt(views.furniture),
         name='furniture'),
    path('furniture/<int:id>/update', csrf_exempt(views.update_furniture),
         name='update_furniture'),
    path('furniture/<int:id>/delete', csrf_exempt(views.delete_furniture),
         name='delete_furniture'),
]
