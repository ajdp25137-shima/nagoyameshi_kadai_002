from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from base.models import Reservation


# 一覧（自分の予約だけ表示）
class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservations/list.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


# 詳細
class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = 'reservations/detail.html'
    context_object_name = 'reservation'


# 作成
class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    fields = ['restaurant', 'reserved_at', 'number_of_people']
    template_name = 'reservations/create.html'
    success_url = reverse_lazy('reservation_list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # ← ここ重要
        return super().form_valid(form)


# 削除
class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'reservations/delete.html'
    success_url = reverse_lazy('reservation_list')