from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, GiftViewSet, InterestViewSet, NotificationViewSet,
    OccasionViewSet, ProfileAPIView, RecommendationAPIView, RecommendationHistoryViewSet,
    WishlistViewSet,
)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('interests', InterestViewSet, basename='interest')
router.register('gifts', GiftViewSet, basename='gift')
router.register('wishlist', WishlistViewSet, basename='wishlist')
router.register('occasions', OccasionViewSet, basename='occasion')
router.register('notifications', NotificationViewSet, basename='notification')
router.register('recommendation-history', RecommendationHistoryViewSet, basename='recommendation-history')

urlpatterns = [
    path('', include(router.urls)),
    path('recommendations/', RecommendationAPIView.as_view(), name='recommendations-api'),
    path('profile/', ProfileAPIView.as_view(), name='profile-api'),
]
