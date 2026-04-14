from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta
from base.models import Reservation, Restaurant

# 一覧（自分の予約だけ表示）
class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservations/list.html'
    context_object_name = 'reservations'
    paginate_by = 10  # 10件ごとに表示

    def get_queryset(self):
        # 自分の予約を、新しい順（reserved_atの降順）に並び替えて取得
        return Reservation.objects.filter(user=self.request.user).order_by('-reserved_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # キャンセル判定（1日前）のために「現在時刻 + 1日」をテンプレートに渡す
        context['cancel_limit'] = timezone.now() + timedelta(days=1)
        return context

# 作成
class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    fields = ['reserved_at', 'number_of_people'] # restaurantは自動設定するのでfieldsから除外
    template_name = 'reservations/create.html'
    success_url = reverse_lazy('reservation_list')

    def form_valid(self, form):
        # URLに含まれる restaurant_id から店舗を取得してセット
        restaurant_id = self.kwargs.get('restaurant_id')
        form.instance.restaurant = Restaurant.objects.get(id=restaurant_id)
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # テンプレートに店舗名を表示するために追加
        context['restaurant'] = Restaurant.objects.get(id=self.kwargs.get('restaurant_id'))
        return context

# 削除（キャンセル用）
class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'reservations/delete.html'
    success_url = reverse_lazy('reservation_list')