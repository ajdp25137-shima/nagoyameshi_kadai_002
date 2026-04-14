from django.urls import path
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
    # トップページ
    # restaurants_view.py 内に top_page 関数がある想定
    path('', top_page, name='top_page'), 

    # 飲食店関連 (restaurants_view.py)
    path('restaurants/', RestaurantListView.as_view(), name='restaurant_list'),
    path('restaurants/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('restaurants/create/', RestaurantCreateView.as_view(), name='restaurant_create'),
    path('restaurants/<int:pk>/update/', RestaurantUpdateView.as_view(), name='restaurant_update'),
    path('restaurants/<int:pk>/delete/', RestaurantDeleteView.as_view(), name='restaurant_delete'),

    # 予約関連 (reservations_view.py)
    path('reservations/', ReservationListView.as_view(), name='reservation_list'),
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation_detail'),
    path('reservations/create/', ReservationCreateView.as_view(), name='reservation_create'),
    path('reservations/<int:pk>/delete/', ReservationDeleteView.as_view(), name='reservation_delete'),

    # お気に入り関連 (favorites_view.py)
    path('favorites/add/<int:restaurant_id>/', FavoriteAddView.as_view(), name='favorite_add'),
    path('favorites/delete/<int:restaurant_id>/', FavoriteDeleteView.as_view(), name='favorite_delete'),

    # カテゴリ関連 (categories_view.py)
    # 必要に応じて追加
    path('categories/', CategoryListView.as_view(), name='category_list'),

    # レビュー関連 (reviews_view.py) なども同様に追加
]