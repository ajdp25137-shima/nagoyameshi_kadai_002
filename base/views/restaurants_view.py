from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from base.models import Restaurant, Category
from django.shortcuts import render


def top_page(request):
    # render関数で、templatesフォルダ内のHTMLを指定します
    return render(request, 'pages/top.html')


# 一覧
class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurants/list.html'
    context_object_name = 'restaurants'


# 詳細
class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurants/detail.html'
    context_object_name = 'restaurant'


# 作成
class RestaurantCreateView(CreateView):
    model = Restaurant
    fields = [
        'category',
        'name',
        'description',
        'phone_number',
        'postal_code',
        'address',
        'open_time',
        'close_time',
        'price_range',
        'seat_capacity',
        'is_active'
    ]
    template_name = 'restaurants/create.html'
    success_url = reverse_lazy('restaurant_list')


# 更新
class RestaurantUpdateView(UpdateView):
    model = Restaurant
    fields = [
        'category',
        'name',
        'description',
        'phone_number',
        'postal_code',
        'address',
        'open_time',
        'close_time',
        'price_range',
        'seat_capacity',
        'is_active'
    ]
    template_name = 'restaurants/update.html'
    success_url = reverse_lazy('restaurant_list')


# 削除
class RestaurantDeleteView(DeleteView):
    model = Restaurant
    template_name = 'restaurants/delete.html'
    success_url = reverse_lazy('restaurant_list')

    