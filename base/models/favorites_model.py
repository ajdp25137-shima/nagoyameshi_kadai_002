from django.db import models
from base.models import User, Restaurant

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='favorites')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "お気に入り"
        verbose_name_plural = "お気に入り"
        # userとrestaurantの組み合わせで一意（重複なし）にする設定
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'restaurant'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        # Userモデルのフィールド名に合わせて調整してください（username or name）
        return f"{self.user.user.email} - {self.restaurant.name}"