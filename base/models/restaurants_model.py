from django.db import models
from .categories_model import Category  # カテゴリモデルを別アプリ想定

class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='restaurants'
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    phone_number = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=10)
    address = models.CharField(max_length=255)

    open_time = models.TimeField()
    close_time = models.TimeField()

    price_range = models.CharField(max_length=50)
    seat_capacity = models.IntegerField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name