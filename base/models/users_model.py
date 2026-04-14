from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager # BaseUserManagerを追加

# 1. ユーザー操作を担当するマネージャーを作成
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('メールアドレスは必須です')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # ハッシュ化して保存
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# 2. ユーザーモデル本体
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # password フィールドは AbstractBaseUser が持っているため、自分で定義しなくてOKです
    postal_code = models.CharField(max_length=10)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)

    # 管理画面へのアクセス許可（これがないとログイン後にエラーになります）
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 重要：ここでマネージャーを紐付ける
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = "会員"          # 単数形での表示名
        verbose_name_plural = "会員"   # 複数形での表示名（日本語なら同じでOK）