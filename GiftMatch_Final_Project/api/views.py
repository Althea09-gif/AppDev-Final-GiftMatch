from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import UserProfile
from gifts.models import Category, Gift, Interest
from occasions.models import Notification, Occasion
from recommendations.models import RecommendationHistory
from wishlist.models import WishlistItem
from .serializers import (
    CategorySerializer, GiftSerializer, InterestSerializer, NotificationSerializer,
    OccasionSerializer, RecommendationHistorySerializer, RecommendationRequestSerializer,
    UserProfileSerializer, WishlistItemSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class InterestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [permissions.AllowAny]


class GiftViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Gift.objects.select_related('category').prefetch_related('interests').all()
    serializer_class = GiftSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        recipient = self.request.query_params.get('recipient')
        occasion = self.request.query_params.get('occasion')
        max_price = self.request.query_params.get('max_price')
        min_price = self.request.query_params.get('min_price')
        interest = self.request.query_params.get('interest')
        store = self.request.query_params.get('store')
        if recipient:
            qs = qs.filter(recipient_type=recipient)
        if occasion:
            qs = qs.filter(occasion_type=occasion)
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)
        if interest:
            qs = qs.filter(interests__name__iexact=interest)
        if store:
            qs = qs.filter(store_name=store)
        return qs.distinct()


class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user).select_related('gift', 'gift__category')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_purchased(self, request, pk=None):
        item = self.get_object()
        item.purchased = not item.purchased
        item.save()
        return Response(self.get_serializer(item).data)


class OccasionViewSet(viewsets.ModelViewSet):
    serializer_class = OccasionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Occasion.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecommendationHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RecommendationHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RecommendationHistory.objects.filter(user=self.request.user).prefetch_related('matched_gifts')


class RecommendationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RecommendationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        history, scored = serializer.create_recommendation(request.user)
        return Response({
            'history': RecommendationHistorySerializer(history).data,
            'results': [
                {
                    'score': item['score'],
                    'reasons': item['reasons'],
                    'why': item.get('why'),
                    'gift': GiftSerializer(item['gift']).data,
                }
                for item in scored[:24]
            ]
        }, status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return Response(UserProfileSerializer(profile).data)

    def put(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
