from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pro/', views.pro, name='pro'),
    path('offline/', views.offline, name='offline'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('contact/', views.contact, name='contact'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('gifts/', include('gifts.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('occasions/', include('occasions.urls')),
    path('notifications/', include('occasions.notification_urls')),
    path('recommendations/', include('recommendations.urls')),
    path('api/v1/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
