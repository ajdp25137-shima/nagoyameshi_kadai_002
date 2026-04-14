from django.views import View
from django.shortcuts import redirect, get_object_or_404
from base.models import Favorite, Restaurant
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView


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

class FavoriteListView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = 'favorites/list.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('restaurant')