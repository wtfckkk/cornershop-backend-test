from rest_framework import routers
from .views import MealsViewSet, MenuViewSet

router = routers.DefaultRouter()

router.register(r'meals', MealsViewSet, basename='meals')
router.register(r'menus', MenuViewSet, basename='menus')
