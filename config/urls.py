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
    path('admin/', admin.site.urls),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('admins/', AdminListView.as_view(), name='admin_list'),
    path('admins/create/', AdminCreateView.as_view(), name='admin_create'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('categories/', include('base.urls')),
    path('restaurants/', include('base.urls')),
    path('reservations/', include('base.urls')),
    path('restaurant/<int:restaurant_id>/reviews/', views.ReviewListView.as_view(), name='review_list'),
    path('restaurant/<int:restaurant_id>/reviews/add/', views.ReviewCreateView.as_view(), name='review_create'),
    path('company/', views.CompanyInformationDetailView.as_view(), name='company_info'),
    path('favorites/', include('base.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)