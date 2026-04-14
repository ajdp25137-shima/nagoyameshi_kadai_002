from django.contrib import admin
from .models import *
from django import forms


# 管理画面に登録
admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(Reservation)
admin.site.register(User)
admin.site.register(Admin)  # Adminモデルも管理画面に登録
admin.site.register(Review)
admin.site.register(CompanyInformation)
admin.site.register(Favorite)

class ReviewAdminForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, f"{'★' * i} ({i})") for i in range(1, 6)],
        label="評価",
    )
    class Meta:
        model = Review
        fields = '__all__'

class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm
    list_display = ('user', 'restaurant', 'rating', 'created_at')