"""geolocation_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from geo_api_app.views import LocationView, AddLocationView, DeleteLocationView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('location/<str:ip_domain>/', LocationView.as_view()),
    path('location/add/<str:ip_domain>/', AddLocationView.as_view()),
    path('location/del/<str:ip_domain>/', DeleteLocationView.as_view()),
    path('location/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('location/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    
]
