from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

# カスタムユーザーモデルを取得
User = get_user_model()

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'auth/profile_detail.html'
    context_object_name = 'user'

    def get_object(self):
        # URL引数のpkを使わず、常にログイン中の自分自身の情報を返す
        return self.request.user

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'auth/profile_edit.html'
    # CustomUserモデルで定義したフィールド名を指定
    fields = ('username', 'email', 'zip_code', 'address', 'phone_number')

    def get_success_url(self):
        # 保存完了後のリダイレクト先（urls.pyのname='top_page'を想定）
        return reverse_lazy('top_page')

    def get_object(self):
        return self.request.user