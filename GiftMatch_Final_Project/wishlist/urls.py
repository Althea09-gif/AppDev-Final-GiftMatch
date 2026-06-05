from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist_list, name='list'),
    path('add/<int:gift_id>/', views.add_to_wishlist, name='add'),
    path('remove/<int:item_id>/', views.remove_from_wishlist, name='remove'),
    path('toggle/<int:item_id>/', views.toggle_purchased, name='toggle'),
]
