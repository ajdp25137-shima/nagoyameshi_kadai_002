from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q, Avg
from base.models import Restaurant, Category, Review


# --- 追加: トップページ用関数 ---
def top_page(request):
    # カテゴリ一覧
    categories = Category.objects.all()

    # 高評価の店舗
    # reviews__score のアンダースコアは必ず「2つ」連続させてください
    top_rated_restaurants = Restaurant.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating')[:5]

    # ランダム表示
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

    # ↓ここから下のインデント（空白4つ分）が正しくクラス内に入っている必要があります
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = self.get_object()
        user = self.request.user

        # 判定フラグの初期化（必ず外側で定義する）
        is_paid = False
        
        if user.is_authenticated:
            # 管理者、または有料会員フラグがTrueの場合
            if user.is_superuser or getattr(user, 'is_paid_member', False):
                is_paid = True
            
            # ターミナルで確認するためのログ
            print(f"DEBUG: User={user}, is_paid={is_paid}")

        # テンプレートで使用する変数
        context['is_paid_member'] = is_paid

        # レビュー取得ロジック
        all_reviews = Review.objects.filter(restaurant=restaurant).order_by('-created_at')
        context['latest_review'] = all_reviews.first()

        if user.is_authenticated:
            my_review = all_reviews.filter(user=user).first()
            context['my_review'] = my_review
            
            if is_paid:
                # 有料会員なら、自分のレビュー以外を表示
                context['other_reviews'] = all_reviews.exclude(id=my_review.id) if my_review else all_reviews
            else:
                context['other_reviews'] = None
        
        return context
    
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