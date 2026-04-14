from django import forms
from base.models import Admin, User, Reservation  # AdminモデルとUserモデルをインポート
from django.contrib.auth.hashers import make_password



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
    
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        # ↓ ここを 'reserved_datetime' から 'reserved_at' に修正
        fields = ['reserved_at', 'number_of_people']
        widgets = {
            # ↓ ここも修正
            'reserved_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'number_of_people': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }