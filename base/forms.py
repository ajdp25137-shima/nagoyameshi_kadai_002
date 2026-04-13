from django import forms
from django.contrib.auth import get_user_model
from base.models import Admin
from django.contrib.auth.hashers import make_password

User = get_user_model()

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="パスワード"
    )

    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'password',
            'postal_code',
            'address',
            'phone_number'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        # パスワードをハッシュ化
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

# Adminモデルのインポート
class AdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Admin
        fields = ['email', 'password']

    def save(self, commit=True):
        admin = super().save(commit=False)
        admin.set_password(self.cleaned_data['password'])
        if commit:
            admin.save()
        return admin