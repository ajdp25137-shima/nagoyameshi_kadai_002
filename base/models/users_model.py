from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('メールアドレスは必須です')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('name', '管理者')
        extra_fields.setdefault('postal_code', '000-0000')
        extra_fields.setdefault('address', '-')
        extra_fields.setdefault('phone_number', '000-0000-0000')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class UserClass(models.TextChoices):
        FREE = "free", "無料会員"
        PREMIUM = "premium", "有料会員"


    name = models.CharField("氏名", max_length=100) # 日本語名を追加
    email = models.EmailField("メールアドレス", unique=True)
    postal_code = models.CharField("郵便番号", max_length=10)
    address = models.TextField("住所")
    phone_number = models.CharField("電話番号", max_length=20)

    user_class = models.CharField(
        "会員区分",
        max_length=10,
        choices=UserClass.choices,
        default=UserClass.FREE

    )

    stripe_customer_id = models.CharField("Stripe顧客ID", max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField("StripeサブスクID", max_length=255, blank=True, null=True)

    # 一般会員側でも「ログイン」は必要だと思うので、is_activeなどは残します
    is_staff = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = "会員"
        verbose_name_plural = "会員"

    def __str__(self):
        return self.email