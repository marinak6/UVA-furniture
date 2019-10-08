from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

app_name = 'models'
urlpatterns = [
    path('bid/create', csrf_exempt(views.createBid), name='create-bid'),
    path('bid/<int:id>', csrf_exempt(views.bid), name='bid'),
    path('bid/<int:id>/delete', csrf_exempt(views.deleteBid), name='delete-bid'),
    path('bid/<int:id>/update', csrf_exempt(views.updateBid), name='update-bid'),
    path('furniture/create', csrf_exempt(views.createFurniture),
         name='createFurniture'),
    path('furniture/<int:id>', csrf_exempt(views.furniture),
         name='furniture'),
    path('furniture/<int:id>/update', csrf_exempt(views.update_furniture),
         name='update_furniture'),
    path('furniture/<int:id>/delete', csrf_exempt(views.delete_furniture),
         name='delete_furniture'),
    path('newest_items', csrf_exempt(views.newest_items),
         name='newest_items'),
]
