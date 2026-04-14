from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class AdminManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Admin(AbstractUser):
    username = None  # usernameを使わない
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this admin belongs to.',
        related_name="admin_groups", # 独自の名前をつける
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this admin.',
        related_name="admin_user_permissions", # 独自の名前をつける,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AdminManager()

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "管理者"          # 単数形での表示名
        verbose_name_plural = "管理者"   # 複数形での表示名（日本語なら同じでOK）