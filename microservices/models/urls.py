from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

app_name = 'models'
urlpatterns = [

    # CREATE
    path('person/create', csrf_exempt(views.create_person), name='create-person'),
    path('bid/create', csrf_exempt(views.createBid), name='create-bid'),
    path('furniture/create', csrf_exempt(views.createFurniture),
         name='createFurniture'),

    # GET and UPDATE
    path('furniture/<int:id>', csrf_exempt(views.furniture), name='furniture'),
    path('furniture/<int:id>/update',
         csrf_exempt(views.update_furniture), name='update_furniture'),
    path('bid/<int:id>', csrf_exempt(views.bid), name='bid'),
    path('bid/<int:id>/update', csrf_exempt(views.updateBid), name='update-bid'),

    # DELETE
    path('furniture/<int:id>/delete',
         csrf_exempt(views.delete_furniture), name='delete_furniture'),
    path('bid/<int:id>/delete', csrf_exempt(views.deleteBid), name='delete-bid'),

    # OTHER
    path('newest_items', csrf_exempt(views.newest_items), name='newest_items'),
    path('get_items', csrf_exempt(views.get_items), name='get_items'),
    path('login', csrf_exempt(views.check_login), name='check-login'),
    path('login/', csrf_exempt(views.check_login), name='check-login'),

    path('logout', csrf_exempt(views.logout), name='logout'),

]
