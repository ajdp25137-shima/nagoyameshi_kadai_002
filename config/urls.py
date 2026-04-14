"""
URL configuration for nagoyameshi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from base.views import UserCreateView, UserListView, AdminListView, AdminCreateView, favorites_view
from base import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # 1. 外部・管理用
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),


    path('profile/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),

    path('company/', views.CompanyInformationDetailView.as_view(), name='company_info'),

    # 3. アプリ全体のURLを一括管理
    # ※ path('favorites/', ...) など、個別の include('base.urls') は全て消してください
    path('', include('base.urls')), 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
