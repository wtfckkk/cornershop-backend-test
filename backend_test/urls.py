"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from rest_framework.authtoken import views
from rest_framework import routers

from meals.urls import router as meals_router
from meals.urls import urlpatterns as meals_urlpatterns
from .utils.healthz import healthz

router = routers.SimpleRouter()
router.registry.extend(meals_router.registry)

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path("healthz", healthz, name="healthz"),
]

urlpatterns += router.urls
urlpatterns += meals_urlpatterns
