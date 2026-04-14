from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q, Avg
from base.models import Restaurant, Category

# --- 追加: トップページ用関数 ---
def top_page(request):
    """
    トップページを表示する関数。
    base/urls.py から呼び出されます。
    """
    # 必要に応じて高評価店などを取得するロジックをここに追加
    return render(request, 'pages/top.html')

# --- 店舗一覧 ---
class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurants/list.html'
    context_object_name = 'restaurants'
    paginate_by = 5

    def get_queryset(self):
        queryset = Restaurant.objects.filter(is_active=True)
        keyword = self.request.GET.get('keyword')
        price_max = self.request.GET.get('price')
        category_id = self.request.GET.get('category')
        order = self.request.GET.get('order')

        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) | Q(description__icontains=keyword)
            )
        if price_max:
            queryset = queryset.filter(price_range__lte=price_max)
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if order == 'price_low':
            queryset = queryset.order_by('price_range')
        elif order == 'rating_high':
            # レビュー機能実装後に有効化
            # queryset = queryset.annotate(avg_rating=Avg('reviews__score')).order_by('-avg_rating')
            pass 
        else:
            # created_at がモデルにない場合は '-id' に書き換えてください
            queryset = queryset.order_by('-id') 

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

# --- 詳細 ---
class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurants/detail.html'
    context_object_name = 'restaurant'

# --- 作成 (画像アップロード対応) ---
class RestaurantCreateView(CreateView):
    model = Restaurant
    fields = [
        'category', 'name', 'image', 'description', 'phone_number', 
        'postal_code', 'address', 'open_time', 'close_time', 
        'price_range', 'seat_capacity', 'is_active'
    ]
    template_name = 'restaurants/create.html'
    success_url = reverse_lazy('restaurant_list')

# --- 更新 ---
class RestaurantUpdateView(UpdateView):
    model = Restaurant
    fields = [
        'category', 'name', 'image', 'description', 'phone_number', 
        'postal_code', 'address', 'open_time', 'close_time', 
        'price_range', 'seat_capacity', 'is_active'
    ]
    template_name = 'restaurants/update.html'
    success_url = reverse_lazy('restaurant_list')

# --- 削除 ---
class RestaurantDeleteView(DeleteView):
    model = Restaurant
    template_name = 'restaurants/delete.html'
    success_url = reverse_lazy('restaurant_list')