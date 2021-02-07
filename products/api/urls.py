from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from products.api.views import OptionModelViewSet, CategoryModelViewSet, ProductModelViewSet

router = DefaultRouter()
router.register('api/option', OptionModelViewSet, basename='api_option')
router.register('api/category', CategoryModelViewSet, basename='api_category')
router.register('api/product', ProductModelViewSet, basename='api_product')

app_name = 'products_api'
urlpatterns = []
urlpatterns += router.urls
