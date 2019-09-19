from django.urls import path
from . import views

app_name = 'models'
urlpatterns = [
    path('bid/create/', views.createBid, name='create-bid'),
]