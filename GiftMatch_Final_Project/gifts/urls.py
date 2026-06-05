from django.urls import path
from . import views

app_name = 'gifts'

urlpatterns = [
    path('finder/', views.finder, name='finder'),
    path('<int:pk>/', views.detail, name='detail'),
]
