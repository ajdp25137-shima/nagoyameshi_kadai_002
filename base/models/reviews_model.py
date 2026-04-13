from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from base.models.restaurants_model import Restaurant  # レストランモデルをインポート

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')

    # 1〜5のバリデーションを追加
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="評価は1以上で入力してください。"),
            MaxValueValidator(5, message="評価は5以下で入力してください。")
        ]
    )

    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name} ({self.rating})"