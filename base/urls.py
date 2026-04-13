from django.urls import path
from .views import CategoryListView
from .views import (
    RestaurantListView,
    RestaurantDetailView,
    RestaurantCreateView,
    RestaurantUpdateView,
    RestaurantDeleteView
)

from .views import (
    ReservationListView,
    ReservationDetailView,
    ReservationCreateView,
    ReservationDeleteView
)

urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),
    path('restaurants/', RestaurantListView.as_view(), name='restaurant_list'),
    path('restaurants/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('restaurants/create/', RestaurantCreateView.as_view(), name='restaurant_create'),
    path('restaurants/<int:pk>/update/', RestaurantUpdateView.as_view(), name='restaurant_update'),
    path('restaurants/<int:pk>/delete/', RestaurantDeleteView.as_view(), name='restaurant_delete'),
    path('reservations/', ReservationListView.as_view(), name='reservation_list'),
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation_detail'),
    path('reservations/create/', ReservationCreateView.as_view(), name='reservation_create'),
    path('reservations/<int:pk>/delete/', ReservationDeleteView.as_view(), name='reservation_delete'),
]