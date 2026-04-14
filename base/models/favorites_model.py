from django.db import models
from base.models import User, Restaurant


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='favorites')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'restaurant')  # 同じ組み合わせの重複防止

    class Meta:
        verbose_name = "お気に入り"
        verbose_name_plural = "お気に入り"

    def __str__(self):
        return f"{self.user.name} - {self.restaurant.name}"