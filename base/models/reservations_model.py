from django.db import models
from django.conf import settings
from .restaurants_model import Restaurant

User = settings.AUTH_USER_MODEL

class Reservation(models.Model):
    id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservations'
    )

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='reservations'
    )

    reserved_at = models.DateTimeField()  # 予約日時
    number_of_people = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.restaurant} ({self.reserved_at})"

    class Meta:
        ordering = ['-reserved_at']