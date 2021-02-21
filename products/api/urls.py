from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from products.api.views import OptionModelViewSet, CategoryModelViewSet, ProductModelViewSet, BrandModelViewSet, \
    CartView, CartViewId, WishView, WishViewId, SearchView, ReviewView

router = DefaultRouter()
router.register('admin/option', OptionModelViewSet, basename='api_admin_option')
router.register('admin/category', CategoryModelViewSet, basename='api_admin_category')
router.register('admin/product', ProductModelViewSet, basename='api_admin_product')
router.register('admin/brand', BrandModelViewSet, basename='api_admin_brand')
router.register('api/search', SearchView, basename='api_search')

app_name = 'products_api'
urlpatterns = router.urls
urlpatterns += [
    path('cart/', CartView.as_view(), name='cart_view'),
    path('cart/<int:pk>/', CartViewId.as_view(), name='cart_delete'),
    path('wish/', WishView.as_view(), name='wish_view'),
    path('wish/<int:pk>/', WishViewId.as_view(), name='wish_delete'),
    path('review/', ReviewView.as_view(), name='review_add'),

]
