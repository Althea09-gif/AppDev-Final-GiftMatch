from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='list'),
    path('mark-read/<int:pk>/', views.notification_mark_read, name='mark_read'),
    path('clear-all/', views.notification_clear_all, name='clear_all'),
]
