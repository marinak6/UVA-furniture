from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'frontend'
urlpatterns = [
    path('', views.home, name='index'),
    path('item/<int:item_id>', views.item_details, name="item_details"),
    path('admin/', admin.site.urls),
    path('create_listing/', views.create_listing, name="create_listing"),
    path('search/', views.search, name='search'),

    # Authentication
    path('register', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# https://stackoverflow.com/questions/44937812/why-is-django-not-loading-my-css
