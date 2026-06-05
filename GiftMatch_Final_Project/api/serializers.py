from rest_framework import serializers
from accounts.models import UserProfile
from gifts.models import Category, Gift, Interest
from occasions.models import Notification, Occasion
from recommendations.engine import score_gifts
from recommendations.models import RecommendationHistory
from wishlist.models import WishlistItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name', 'icon']


class GiftSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    interests = InterestSerializer(many=True, read_only=True)

    class Meta:
        model = Gift
        fields = [
            'id', 'name', 'description', 'category', 'recipient_type', 'occasion_type',
            'interests', 'minimum_budget', 'maximum_budget', 'price', 'product_image',
            'store_link', 'store_name', 'is_featured', 'rating', 'created_at'
        ]


class WishlistItemSerializer(serializers.ModelSerializer):
    gift = GiftSerializer(read_only=True)
    gift_id = serializers.PrimaryKeyRelatedField(queryset=Gift.objects.all(), write_only=True, source='gift')

    class Meta:
        model = WishlistItem
        fields = ['id', 'gift', 'gift_id', 'purchased', 'notes', 'created_at', 'updated_at']


class OccasionSerializer(serializers.ModelSerializer):
    days_left = serializers.IntegerField(read_only=True)
    reminder_date = serializers.DateField(read_only=True)

    class Meta:
        model = Occasion
        fields = [
            'id', 'event_title', 'recipient_name', 'occasion_type', 'event_date',
            'reminder_days_before', 'notes', 'days_left', 'reminder_date', 'created_at', 'updated_at'
        ]


class NotificationSerializer(serializers.ModelSerializer):
    gift = GiftSerializer(read_only=True)
    occasion = OccasionSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'notification_type', 'title', 'message', 'occasion', 'gift', 'is_read', 'created_at']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'full_name', 'bio', 'avatar_url', 'favorite_color', 'preferred_budget_min', 'preferred_budget_max']


class RecommendationHistorySerializer(serializers.ModelSerializer):
    matched_gifts = GiftSerializer(many=True, read_only=True)

    class Meta:
        model = RecommendationHistory
        fields = ['id', 'recipient_type', 'occasion_type', 'interest_summary', 'budget_min', 'budget_max', 'matched_gifts', 'created_at']


class RecommendationRequestSerializer(serializers.Serializer):
    recipient_type = serializers.CharField()
    occasion_type = serializers.CharField()
    interest_ids = serializers.ListField(child=serializers.IntegerField(), required=False, default=list)
    budget_min = serializers.DecimalField(max_digits=10, decimal_places=2)
    budget_max = serializers.DecimalField(max_digits=10, decimal_places=2)
    marketplace = serializers.CharField(required=False, allow_blank=True, default='any')

    def create_recommendation(self, user):
        interests = list(Interest.objects.filter(id__in=self.validated_data.get('interest_ids', [])))
        scored = score_gifts(
            self.validated_data['recipient_type'],
            self.validated_data['occasion_type'],
            interests,
            float(self.validated_data['budget_min']),
            float(self.validated_data['budget_max']),
            self.validated_data.get('marketplace') or 'any',
        )
        history = RecommendationHistory.objects.create(
            user=user,
            recipient_type=self.validated_data['recipient_type'],
            occasion_type=self.validated_data['occasion_type'],
            interest_summary=', '.join([i.name for i in interests]),
            budget_min=self.validated_data['budget_min'],
            budget_max=self.validated_data['budget_max'],
        )
        history.matched_gifts.set([item['gift'] for item in scored[:24]])
        return history, scored
