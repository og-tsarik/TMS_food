"""
URL configuration for food project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from app.views import home
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('', home, name="home"),
    path('admin/', admin.site.urls),
    path("api/recipes/", include("app.api.urls")),
    # Token
    path("api/auth/", include("djoser.urls.authtoken")),
    # path("api/auth/", include("djoser.urls")),  # Чтобы заработали прописанные в документации urls (/me и т.д.)
    path("api/auth/", include("djoser.urls.jwt")),
    path("api/auth/", include("djoser.urls.base")),
    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # Other
    # связь с приложением 'users':
    path("account/", include('users.urls')),  # Если в url будет 'account/', то перейдёт (include) в 'users.urls'
    # связь с приложением 'app'
    path("recipe/", include('app.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls'))
]
