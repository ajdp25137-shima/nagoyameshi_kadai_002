from django.views import View
from django.shortcuts import redirect, get_object_or_404
from base.models import Favorite, Restaurant
from django.contrib.auth.mixins import LoginRequiredMixin


class FavoriteAddView(LoginRequiredMixin, View):
    def post(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        Favorite.objects.get_or_create(
            user=request.user,
            restaurant=restaurant
        )

        return redirect('restaurant_detail', restaurant_id=restaurant.id)

class FavoriteDeleteView(LoginRequiredMixin, View):
    def post(self, request, restaurant_id):
        Favorite.objects.filter(
            user=request.user,
            restaurant_id=restaurant_id
        ).delete()

        return redirect('restaurant_detail', restaurant_id=restaurant_id)