from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from base.models import Review, Restaurant

class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        # 特定の飲食店のレビューのみ取得する場合
        return Review.objects.filter(restaurant_id=self.kwargs['restaurant_id']).order_by('-created_at')

class ReviewCreateView(CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'reviews/review_form.html'

    def form_valid(self, form):
        # ログインユーザーと対象の飲食店を自動的にセット
        form.instance.user = self.request.user
        form.instance.restaurant = get_object_or_404(Restaurant, pk=self.kwargs['restaurant_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('restaurant_detail', kwargs={'pk': self.kwargs['restaurant_id']})