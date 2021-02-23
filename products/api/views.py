from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from products.api.serializers import OptionSerializer, CategorySerializer, ProductSerializer, BrandSerializer, \
    CartSerializer, WishSerializer, ReviewSerializer
from products.models import Product, Option, Category, Brand, Cart, CartProduct, WishList
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

field_expand = [
    openapi.Parameter('expand', in_=openapi.IN_QUERY,
                      description='Set up fields that be expanded to their fully serialized counterparts via query '
                                  'parameters',
                      type=openapi.TYPE_STRING),
    openapi.Parameter('fields', in_=openapi.IN_QUERY,
                      description='A query with the fields parameter on the other hand returns only a subset of the '
                                  'fields',
                      type=openapi.TYPE_STRING),
    openapi.Parameter('omit', in_=openapi.IN_QUERY,
                      description='A query with the omit parameter excludes specified fields',
                      type=openapi.TYPE_STRING)]
create = [
    openapi.Parameter('images', in_=openapi.IN_FORM, description='multi files of Product images you want to add',
                      type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_FILE))]
update = create + [
    openapi.Parameter('del_img', in_=openapi.IN_FORM, description='list of ids of Product images you want to delete',
                      type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER)),]


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


# Admin APIs Views
@method_decorator(permission_required('products.view_option', raise_exception=True), name='list')
@method_decorator(permission_required('products.view_option', raise_exception=True), name='retrieve')
class OptionModelViewSet(ModelViewSet):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()
    permission_classes = [DjangoObjectPermissions]
    pagination_class = StandardResultsSetPagination


@method_decorator(permission_required('products.view_category', raise_exception=True), name='list')
@method_decorator(permission_required('products.view_category', raise_exception=True), name='retrieve')
class CategoryModelViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [DjangoObjectPermissions]
    pagination_class = StandardResultsSetPagination


@method_decorator(permission_required('products.view_category', raise_exception=True), name='list')
@method_decorator(permission_required('products.view_category', raise_exception=True), name='retrieve')
class BrandModelViewSet(ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    permission_classes = [DjangoObjectPermissions]
    pagination_class = StandardResultsSetPagination


@method_decorator(name='update', decorator=swagger_auto_schema(manual_parameters=update))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(manual_parameters=update))
@method_decorator(name='create', decorator=swagger_auto_schema(manual_parameters=create))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(manual_parameters=field_expand))
@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=field_expand))
@method_decorator(permission_required('products.view_product', raise_exception=True), name='list')
@method_decorator(permission_required('products.view_product', raise_exception=True), name='retrieve')
class ProductModelViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [DjangoObjectPermissions]
    pagination_class = StandardResultsSetPagination


# End Admin APIs Views


# Site APIs Views
class CartView(APIView):
    serializer_class = CartSerializer

    # overwrite get_parsers for put function to parse as Json not FormData
    def get_parsers(self):
        if self.request.method == 'POST':
            return [parser() for parser in [JSONParser]]
        else:
            return super(CartView, self).get_parsers()

    def get_object(self):
        if self.request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=self.request.user)[0]
        else:
            if not self.request.session.exists(self.request.session.session_key):
                self.request.session.create()
            cart = Cart.objects.get_or_create(session_key=self.request.session.session_key)[0]
        return cart

    @swagger_auto_schema(operation_id='cart_read', responses={200: CartSerializer})
    def get(self, request):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    @swagger_auto_schema(operation_id='cart_create_update', request_body=CartSerializer,
                         operation_description='If you send a product in cart , you can update quantity and if you '
                                               'send `quantity = "plus"` ,you update quantity +=1',
                         operation_summary='You Can Send More Than One Product In Same Time',
                         responses={200: CartSerializer})
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CartViewId(APIView):
    serializer_class = CartSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=self.request.user)[0]
        else:
            if not self.request.session.exists(self.request.session.session_key):
                self.request.session.create()
            cart = Cart.objects.get_or_create(session_key=self.request.session.session_key)[0]
        return cart

    @swagger_auto_schema(operation_id='cart_delete', responses={200: CartSerializer})
    def delete(self, request, pk):
        cart = self.get_object()
        product = Product.view_object.get(id=pk)
        if product:
            try:
                cp = CartProduct.objects.get(cart=cart, product_id=product)
                cp.delete()
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(cart)
        return Response(serializer.data)


class WishView(APIView):
    serializer_class = WishSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            wish = WishList.objects.get_or_create(user=self.request.user)[0]
        else:
            if not self.request.session.exists(self.request.session.session_key):
                self.request.session.create()
            wish = WishList.objects.get_or_create(session_key=self.request.session.session_key)[0]
        return wish

    @swagger_auto_schema(operation_id='wish_read', responses={200: WishSerializer})
    def get(self, request):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    @swagger_auto_schema(operation_id='wish_create', request_body=WishSerializer,
                         responses={200: WishSerializer},
                         operation_summary='You Can Send More Than One Product In Same Time', )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class WishViewId(APIView):
    serializer_class = WishSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            wish = WishList.objects.get_or_create(user=self.request.user)[0]
        else:
            if not self.request.session.exists(self.request.session.session_key):
                self.request.session.create()
            wish = WishList.objects.get_or_create(session_key=self.request.session.session_key)[0]
        return wish

    @swagger_auto_schema(operation_id='wish_delete', responses={200: WishSerializer})
    def delete(self, request, pk):
        wish = self.get_object()
        product = Product.view_object.get(id=pk)
        if product in wish.products.all():
            # remove product from wish list just one time
            wish.products.remove(product)
        serializer = self.serializer_class(wish)
        return Response(serializer.data)


@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=field_expand))
class SearchView(mixins.ListModelMixin, GenericViewSet):
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Product.view_object.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'sku': ['exact'],
        'price': ['gte', 'lte'],
        'name': ['icontains'],
        'name_ar': ['icontains'],
        'categories': ['exact'],
        'options': ['exact'],
        'brand': ['exact'],
        'rate': ['gte', 'lte'],
    }
    search_fields = ['name', 'name_ar', 'categories__name', 'categories__name_ar', 'options__name', 'options__name_ar',
                     'sku', ]
    ordering_fields = ['price', 'rate']
    ordering = ['rate']


class ReviewView(APIView):
    serializer_class = ReviewSerializer

    @swagger_auto_schema(request_body=ReviewSerializer, responses={200: ReviewSerializer})
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@method_decorator(name='retrieve', decorator=swagger_auto_schema(manual_parameters=field_expand))
class ProductView(mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = ProductSerializer
    queryset = Product.view_object.all()
