from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import OptionUpdateView, OptionCreateView, OptionDetailView, OptionListView, OptionListJson, \
    ProductCreateView, ProductDetailView, ProductUpdateView, ProductListJson, ProductListView, CategoryListView, \
    CategoryDetailView, CategoryCreateView, CategoryListJson, CategoryUpdateView, ProductDeleteView, CategoryDeleteView, \
    OptionDeleteView, BrandListView, BrandListJson, BrandDetailView, BrandUpdateView, BrandCreateView, BrandDeleteView, \
    ProductView, add_cart, add_wish, ShopView

app_name = 'products'
urlpatterns = [
    # Option Admin Urls
    path('seller/option/', OptionListView.as_view(), name='option_list'),
    path('seller/option/data/', OptionListJson.as_view(), name='option_list_data'),
    path('seller/option/<int:pk>/', OptionDetailView.as_view(), name='option_detail'),
    path('seller/option/update/<int:pk>/', OptionUpdateView.as_view(), name='option_update'),
    path('seller/option/add', OptionCreateView.as_view(), name='option_add'),
    path('seller/option/delete/<int:pk>', OptionDeleteView.as_view(), name='option_delete'),

    # Category Admin Urls
    path('seller/category/', CategoryListView.as_view(), name='category_list'),
    path('seller/category/data/', CategoryListJson.as_view(), name='category_list_data'),
    path('seller/category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('seller/category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('seller/category/add', CategoryCreateView.as_view(), name='category_add'),
    path('seller/category/delete/<int:pk>', CategoryDeleteView.as_view(), name='category_delete'),

    # Brand Admin Urls
    path('seller/brand/', BrandListView.as_view(), name='brand_list'),
    path('seller/brand/data/', BrandListJson.as_view(), name='brand_list_data'),
    path('seller/brand/<int:pk>/', BrandDetailView.as_view(), name='brand_detail'),
    path('seller/brand/update/<int:pk>/', BrandUpdateView.as_view(), name='brand_update'),
    path('seller/brand/add', BrandCreateView.as_view(), name='brand_add'),
    path('seller/brand/delete/<int:pk>', BrandDeleteView.as_view(), name='brand_delete'),

    # Product Admin Urls
    path('seller/product/', ProductListView.as_view(), name='product_list'),
    path('seller/product/data/', ProductListJson.as_view(), name='product_list_data'),
    path('seller/product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('seller/product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('seller/product/add', ProductCreateView.as_view(), name='product_add'),
    path('seller/product/delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete'),

    # Product Api
    path('', include('products.api.urls', namespace='products_api')),

    # Site Urls
    path('product/<int:pk>/', ProductView.as_view(), name='product'),

    # Ajax Add to cart
    path('ajax/add_cart/', add_cart, name='add_cart'),
    # Ajax Add to wishlist
    path('ajax/add_wish/', add_wish, name='add_wish'),
    # Shop View
    path('shop/', ShopView.as_view(), name='shop')
    # End Site Urls
]
