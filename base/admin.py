from django.contrib import admin
from .models import *  # すべてのモデルをインポート

# 管理画面に登録
admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(Reservation)
admin.site.register(User)
admin.site.register(Admin)  # Adminモデルも管理画面に登録
admin.site.register(Review)
admin.site.register(CompanyInformation)
admin.site.register(Favorite)