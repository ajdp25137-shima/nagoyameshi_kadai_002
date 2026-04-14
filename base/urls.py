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
from .views import top_page

urlpatterns = [
    path('', top_page, name='top_page'),

    ## --- サブスクリプション関連 ---
    # 1. 登録ページ表示用（URLをこれ1本に絞る）
    path('subscription/register/', views.SubscriptionCreateView.as_view(), name='subscription_create'),

    # 2. 完了ページ
    path('subscription/complete/', views.SubscriptionCompleteView.as_view(), name='subscription_complete'),

    # 3. StripeのIntent作成（API用：URLを完全に分ける）
    path('subscription/create-intent/', views.CreatePaymentIntentView.as_view(), name='create_setup_intent'),

    # 4. 解約・支払い変更
    path('subscription/cancel/', views.SubscriptionCancelView.as_view(), name='subscription_cancel'),
    path('subscription/cancel/complete/', views.SubscriptionCancelCompleteView.as_view(), name='subscription_cancel_complete'),
    path('subscription/payment/', views.PaymentMethodUpdateView.as_view(), name='payment_update'),
    path('subscription/payment/complete/', views.PaymentUpdateCompleteView.as_view(), name='payment_update_complete'),

    # 飲食店
    path('list/', views.RestaurantListView.as_view(), name='restaurant_list'),
    path('restaurants/<int:pk>/', views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    # レビューはここ（base/urls.py）で管理する方がミスが減ります
    path('restaurant/<int:restaurant_id>/reviews/', views.ReviewListView.as_view(), name='review_list'),
    path('restaurant/<int:restaurant_id>/reviews/add/', views.ReviewCreateView.as_view(), name='review_form'),

    # お気に入り（これで URL は /favorites/ になります）
    path('favorites/', FavoriteListView.as_view(), name='favorite_list'),
    path('favorites/add/<int:restaurant_id>/', FavoriteAddView.as_view(), name='favorite_add'),
    path('favorites/delete/<int:restaurant_id>/', FavoriteDeleteView.as_view(), name='favorite_delete'),

    # 予約関連 (reservations_view.py)
    path('reservations/', ReservationListView.as_view(), name='reservation_list'),
    path('restaurants/<int:restaurant_id>/reserve/', views.ReservationCreateView.as_view(), name='reservation_create'),
    path('reservations/<int:pk>/delete/', ReservationDeleteView.as_view(), name='reservation_delete'),

    # カテゴリ関連 (categories_view.py)
    # 必要に応じて追加
    path('categories/', CategoryListView.as_view(), name='category_list'),

    # レビュー関連 (reviews_view.py) なども同様に追加
]