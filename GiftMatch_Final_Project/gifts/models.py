from django.db import models
from .choices import OCCASION_CHOICES, RECIPIENT_CHOICES, STORE_CHOICES


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Interest(models.Model):
    name = models.CharField(max_length=80, unique=True)
    icon = models.CharField(max_length=40, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Gift(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='gifts')
    recipient_type = models.CharField(max_length=30, choices=RECIPIENT_CHOICES)
    occasion_type = models.CharField(max_length=30, choices=OCCASION_CHOICES)
    interests = models.ManyToManyField(Interest, related_name='gifts', blank=True)
    minimum_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maximum_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.CharField(max_length=255, blank=True, help_text='Static image path or image URL')
    store_link = models.URLField(blank=True)
    store_name = models.CharField(max_length=40, choices=STORE_CHOICES, default='Other')
    is_featured = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'price', 'name']

    def __str__(self):
        return self.name

    @property
    def interest_list(self):
        return ', '.join(self.interests.values_list('name', flat=True))
