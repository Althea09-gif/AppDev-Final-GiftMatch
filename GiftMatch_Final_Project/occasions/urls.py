from django.urls import path
from . import views

app_name = 'occasions'

urlpatterns = [
    path('', views.occasion_list, name='list'),
    path('<int:pk>/edit/', views.occasion_edit, name='edit'),
    path('<int:pk>/delete/', views.occasion_delete, name='delete'),
]
