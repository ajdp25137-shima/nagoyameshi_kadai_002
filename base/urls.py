from django.urls import path
from . import views
# 各ビューファイルからすべてインポート
from .views.users_view import *
from .views.admins_view import *
from .views.categories_view import *
from .views.restaurants_view import *
from .views.reservations_view import *
from .views.reviews_view import *
from .views.company_informations_view import *
from .views.favorites_view import *

urlpatterns = [
    path('', top_page, name='top_page'), 

    # 飲食店
    path('restaurants/', RestaurantListView.as_view(), name='restaurant_list'),
    path('restaurants/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant_detail'),
    # レビューはここ（base/urls.py）で管理する方がミスが減ります
    path('restaurant/<int:restaurant_id>/reviews/', views.ReviewListView.as_view(), name='review_list'),
    path('restaurant/<int:restaurant_id>/reviews/add/', views.ReviewCreateView.as_view(), name='review_create'),

    # お気に入り（これで URL は /favorites/ になります）
    path('favorites/', FavoriteListView.as_view(), name='favorite_list'),
    path('favorites/add/<int:restaurant_id>/', FavoriteAddView.as_view(), name='favorite_add'),
    path('favorites/delete/<int:restaurant_id>/', FavoriteDeleteView.as_view(), name='favorite_delete'),

    # 予約関連 (reservations_view.py)
    path('reservations/', ReservationListView.as_view(), name='reservation_list'),
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation_detail'),
    path('reservations/create/', ReservationCreateView.as_view(), name='reservation_create'),
    path('reservations/<int:pk>/delete/', ReservationDeleteView.as_view(), name='reservation_delete'),

    # カテゴリ関連 (categories_view.py)
    # 必要に応じて追加
    path('categories/', CategoryListView.as_view(), name='category_list'),

    # レビュー関連 (reviews_view.py) なども同様に追加
]