from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q, Avg
from django.contrib.auth.mixins import LoginRequiredMixin
# Favorite モデルをインポート（アプリ構成に合わせて変更してください）
from base.models import Restaurant, Category, Review, Favorite 

# --- 追加: トップページ用関数 ---
def top_page(request):
    categories = Category.objects.all()
    # 修正: reviews__rating -> reviews__score (Reviewモデルのフィールド名に合わせてください)
    top_rated_restaurants = Restaurant.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating')[:5]
    random_restaurants = Restaurant.objects.order_by('?')[:5]

    context = {
        'categories': categories,
        'top_rated_restaurants': top_rated_restaurants,
        'random_restaurants': random_restaurants,
    }
    return render(request, 'pages/top.html', context)

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
            queryset = queryset.annotate(avg_rating=Avg('reviews__score')).order_by('-avg_rating')
        else:
            queryset = queryset.order_by('-id') 
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

# --- 詳細ページ（お気に入り判定を追加） ---
class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurants/detail.html'
    context_object_name = 'restaurant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = self.get_object()
        user = self.request.user

        is_paid_member = False
        is_favorite = False # お気に入り判定の初期化
        
        if user.is_authenticated:
            # 有料会員判定
            if user.is_superuser or getattr(user, 'is_paid_member', False):
                is_paid_member  = True
                # 有料会員の場合のみ、お気に入り登録済みかチェック
                is_favorite = Favorite.objects.filter(user=user, restaurant=restaurant).exists()

        context['is_paid_member'] = is_paid_member
        context['is_favorite'] = is_favorite # テンプレートに渡す

        # レビュー取得
        all_reviews = Review.objects.filter(restaurant=restaurant).order_by('-created_at')
        context['latest_review'] = all_reviews.first()

        if user.is_authenticated:
            my_review = all_reviews.filter(user=user).first()
            context['my_review'] = my_review
            if is_paid_member:
                context['other_reviews'] = all_reviews.exclude(id=my_review.id) if my_review else all_reviews
            else:
                context['other_reviews'] = None
        
        return context

# --- お気に入り追加/削除/一覧のView ---

def favorite_create(request, restaurant_id):
    """お気に入りに追加"""
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    # 有料会員のみ許可
    if getattr(request.user, 'is_paid_member', False) or request.user.is_superuser:
        Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)
    return redirect('restaurant_detail', pk=restaurant_id)

def favorite_delete(request, restaurant_id):
    """お気に入りから削除"""
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    favorite = Favorite.objects.filter(user=request.user, restaurant=restaurant)
    if favorite.exists():
        favorite.delete()
    # 元のページ（詳細または一覧）に戻る
    return redirect(request.META.get('HTTP_REFERER', 'restaurant_detail'))

class FavoriteListView(LoginRequiredMixin, ListView):
    """お気に入り一覧（マイページ用）"""
    model = Favorite
    template_name = 'favorites/favorite_list.html'
    context_object_name = 'favorites'
    paginate_by = 10

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).order_by('-created_at')

# --- 作成・更新・削除（既存のまま） ---
class RestaurantCreateView(CreateView):
    model = Restaurant
    fields = ['category', 'name', 'image', 'description', 'phone_number', 'postal_code', 'address', 'open_time', 'close_time', 'price_range', 'seat_capacity', 'is_active']
    template_name = 'restaurants/create.html'
    success_url = reverse_lazy('restaurant_list')

class RestaurantUpdateView(UpdateView):
    model = Restaurant
    fields = ['category', 'name', 'image', 'description', 'phone_number', 'postal_code', 'address', 'open_time', 'close_time', 'price_range', 'seat_capacity', 'is_active']
    template_name = 'restaurants/update.html'
    success_url = reverse_lazy('restaurant_list')

class RestaurantDeleteView(DeleteView):
    model = Restaurant
    template_name = 'restaurants/delete.html'
    success_url = reverse_lazy('restaurant_list')