from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from base.models import Review, Restaurant
from django.contrib.auth.mixins import LoginRequiredMixin


class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/list.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        # 特定の飲食店のレビューのみ取得する場合
        return Review.objects.filter(user_id=self.kwargs['user_id']).order_by('-created_at')

class ReviewCreateView(CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'reviews/form.html'

    def form_valid(self, form):
        # ログインユーザーと対象の飲食店を自動的にセット
        form.instance.user = self.request.user
        form.instance.restaurant = get_object_or_404(Restaurant, pk=self.kwargs['restaurant_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('restaurant_detail', kwargs={'pk': self.kwargs['restaurant_id']})

class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ['rating', 'comment'] # 実際のモデルのフィールド名に合わせてください
    template_name = 'reviews/form.html'

def get_success_url(self):
# 投稿後、その店舗の詳細ページにリダイレクトする
    return reverse_lazy('restaurant_detail', kwargs={'pk': self.object.restaurant.pk})

class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'

def get_success_url(self):
    return reverse_lazy('restaurant_detail', kwargs={'pk': self.object.restaurant.pk})