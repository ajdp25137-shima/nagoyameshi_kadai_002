from django.views import View
from django.shortcuts import redirect, get_object_or_404
from base.models import Favorite, Restaurant
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

class FavoriteAddView(LoginRequiredMixin, View):
    def post(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        Favorite.objects.get_or_create(
            user=request.user,
            restaurant=restaurant
        )

        # 修正箇所：restaurant_id= を pk= に変更
        return redirect('restaurant_detail', pk=restaurant.id)

class FavoriteDeleteView(LoginRequiredMixin, View):
    def post(self, request, restaurant_id):
        Favorite.objects.filter(
            user=request.user,
            restaurant_id=restaurant_id
        ).delete()

        # 修正箇所：restaurant_id= を pk= に変更
        return redirect('restaurant_detail', pk=restaurant_id)

class FavoriteListView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = 'favorites/list.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('restaurant')