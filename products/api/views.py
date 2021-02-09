from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.viewsets import ModelViewSet
from products.api.serializers import OptionSerializer, CategorySerializer, ProductSerializer, BrandSerializer
from products.models import Product, Option, Category, Brand


class OptionModelViewSet(ModelViewSet):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()
    permission_classes = [DjangoObjectPermissions]

    # override list and retrieve function because DjangoObjectPermissions not have permission on get request (view)
    @method_decorator(permission_required('products.view_option', raise_exception=True), name='dispatch')
    def list(self, request, *args, **kwargs):
        return super(OptionModelViewSet, self).list(request, *args, **kwargs)

    @method_decorator(permission_required('products.view_option', raise_exception=True), name='dispatch')
    def retrieve(self, request, *args, **kwargs):
        return super(OptionModelViewSet, self).retrieve(request, *args, **kwargs)


class CategoryModelViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [DjangoObjectPermissions]

    # override list and retrieve function because DjangoObjectPermissions not have permission on get request (view)
    @method_decorator(permission_required('products.view_category', raise_exception=True), name='dispatch')
    def list(self, request, *args, **kwargs):
        return super(CategoryModelViewSet, self).list(request, *args, **kwargs)

    @method_decorator(permission_required('products.view_category', raise_exception=True), name='dispatch')
    def retrieve(self, request, *args, **kwargs):
        return super(CategoryModelViewSet, self).retrieve(request, *args, **kwargs)


class BrandModelViewSet(ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    permission_classes = [DjangoObjectPermissions]

    # override list and retrieve function because DjangoObjectPermissions not have permission on get request (view)
    @method_decorator(permission_required('products.view_category', raise_exception=True), name='dispatch')
    def list(self, request, *args, **kwargs):
        return super(BrandModelViewSet, self).list(request, *args, **kwargs)

    @method_decorator(permission_required('products.view_category', raise_exception=True), name='dispatch')
    def retrieve(self, request, *args, **kwargs):
        return super(BrandModelViewSet, self).retrieve(request, *args, **kwargs)


class ProductModelViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [DjangoObjectPermissions]

    # override list and retrieve function because DjangoObjectPermissions not have permission on get request (view)
    @method_decorator(permission_required('products.view_product', raise_exception=True), name='dispatch')
    def list(self, request, *args, **kwargs):
        return super(ProductModelViewSet, self).list(request, *args, **kwargs)

    @method_decorator(permission_required('products.view_product', raise_exception=True), name='dispatch')
    def retrieve(self, request, *args, **kwargs):
        return super(ProductModelViewSet, self).retrieve(request, *args, **kwargs)
