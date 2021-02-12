import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django import forms
from django.http import JsonResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (TemplateView, DetailView, CreateView, UpdateView, DeleteView, ListView)
from django_datatables_view.base_datatable_view import BaseDatatableView
from .models import Option, Product, Category, ProductImages, Brand, Cart, CartProduct, WishList
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _


# delete function used in list Views for multiple deletion
def multi_delete(request, model):
    ids = request.POST.get('deleteIds', None)
    if ids:
        ids = ids.split(',')
        mod = model.objects.filter(pk__in=ids)
        if mod:
            for m in mod:
                m.delete()


# Admin Dashboard Views
# Option Views
@method_decorator(permission_required('products.view_option', raise_exception=True), name='dispatch')
class OptionListView(LoginRequiredMixin, TemplateView):
    template_name = 'AdminLte/option/list.html'

    # for post request in delete
    @method_decorator(permission_required('products.delete_option', raise_exception=True), name='dispatch')
    def post(self, request):
        multi_delete(request, Option)
        return redirect('products:option_list')


@method_decorator(permission_required('products.view_option', raise_exception=True), name='dispatch')
class OptionListJson(LoginRequiredMixin, BaseDatatableView):
    columns = ['id', 'name', 'name_ar', 'description', 'description_ar']
    order_columns = ['id', 'name', 'name_ar', 'description', 'description_ar']
    max_display_length = 30

    def get_initial_queryset(self):
        return Option.objects.all().order_by('-created_at')

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(name_ar__icontains=search) |
                Q(description__icontains=search) |
                Q(description_ar__icontains=search)
            )
        return qs


@method_decorator(permission_required('products.view_option', raise_exception=True), name='dispatch')
class OptionDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'option'
    model = Option
    template_name = 'AdminLte/option/detail.html'


@method_decorator(permission_required('products.add_option', raise_exception=True), name='dispatch')
class OptionCreateView(LoginRequiredMixin, CreateView):
    fields = ('name', 'name_ar', 'description', 'description_ar')
    model = Option
    template_name = 'AdminLte/option/form.html'

    def get_form(self, form_class=None):
        form = super(OptionCreateView, self).get_form()
        form.fields['description'] = forms.CharField(widget=forms.Textarea)
        form.fields['description_ar'] = forms.CharField(widget=forms.Textarea)
        return form

    def get_success_url(self):
        if self.request.POST.get('another', None):
            return reverse_lazy('products:option_add')
        return reverse_lazy('products:option_detail', kwargs={'pk': self.object.pk})


@method_decorator(permission_required('products.change_option', raise_exception=True), name='dispatch')
class OptionUpdateView(LoginRequiredMixin, UpdateView):
    fields = ('name', 'name_ar', 'description', 'description_ar')
    model = Option
    template_name = 'AdminLte/option/form.html'

    def get_form(self, form_class=None):
        form = super(OptionUpdateView, self).get_form()
        form.fields['description'] = forms.CharField(widget=forms.Textarea)
        form.fields['description_ar'] = forms.CharField(widget=forms.Textarea)
        return form

    def get_success_url(self):
        return reverse_lazy('products:option_detail', kwargs={'pk': self.object.pk})


@method_decorator(permission_required('products.delete_option', raise_exception=True), name='dispatch')
class OptionDeleteView(LoginRequiredMixin, DeleteView):
    model = Option
    success_url = reverse_lazy('products:option_list')
    template_name = 'AdminLte/option/delete.html'


# Category Views
@method_decorator(permission_required('products.view_category', raise_exception=True), name='dispatch')
class CategoryListView(LoginRequiredMixin, TemplateView):
    template_name = 'AdminLte/category/list.html'

    # for post request in delete
    @method_decorator(permission_required('products.delete_category', raise_exception=True), name='dispatch')
    def post(self, request):
        multi_delete(request, Category)
        return redirect('products:category_list')


@method_decorator(permission_required('products.view_category', raise_exception=True), name='dispatch')
class CategoryListJson(LoginRequiredMixin, BaseDatatableView):
    columns = ['id', 'name', 'name_ar', 'description', 'description_ar', 'image']
    order_columns = ['id', 'name', 'name_ar', 'description', 'description_ar', 'image']
    max_display_length = 30
    model = Category

    def render_column(self, row, column):
        if column == 'image':
            return str(row.image.url)
        else:
            return super().render_column(row, column)

    def get_initial_queryset(self):
        return Category.objects.all().order_by('-created_at')

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(name_ar__icontains=search) |
                Q(description__icontains=search) |
                Q(description_ar__icontains=search)
            )
        return qs


@method_decorator(permission_required('products.view_category', raise_exception=True), name='dispatch')
class CategoryDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'category'
    model = Category
    template_name = 'AdminLte/category/detail.html'


@method_decorator(permission_required('products.add_category', raise_exception=True), name='dispatch')
class CategoryCreateView(LoginRequiredMixin, CreateView):
    fields = ('name', 'name_ar', 'description', 'description_ar', 'image')
    model = Category
    template_name = 'AdminLte/category/form.html'

    # to edit form fields that class generate
    def get_form(self, form_class=None):
        form = super(CategoryCreateView, self).get_form()
        form.fields['description'] = forms.CharField(widget=forms.Textarea)
        form.fields['description_ar'] = forms.CharField(widget=forms.Textarea)
        # overwrite template name of image filed widget to customize design
        form.fields['image'].widget.template_name = 'AdminLte/clearable_file_input.html'
        return form

    def get_success_url(self):
        if self.request.POST.get('another', None):
            return reverse_lazy('products:category_add')
        return reverse_lazy('products:category_detail', kwargs={'pk': self.object.pk})


@method_decorator(permission_required('products.change_category', raise_exception=True), name='dispatch')
class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    fields = ('name', 'name_ar', 'description', 'description_ar', 'image')
    model = Category
    template_name = 'AdminLte/category/form.html'

    # to edit form fields that class generate
    def get_form(self, form_class=None):
        form = super(CategoryUpdateView, self).get_form()
        form.fields['description'] = forms.CharField(widget=forms.Textarea)
        form.fields['description_ar'] = forms.CharField(widget=forms.Textarea)
        # overwrite template name of image filed widget to customize design
        form.fields['image'].widget.template_name = 'AdminLte/clearable_file_input.html'
        return form

    def get_success_url(self):
        return reverse_lazy('products:category_detail', kwargs={'pk': self.object.pk})


@method_decorator(permission_required('products.delete_category', raise_exception=True), name='dispatch')
class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('products:category_list')
    template_name = 'AdminLte/category/delete.html'


# Brand Views
@method_decorator(permission_required('products.view_brand', raise_exception=True), name='dispatch')
class BrandListView(LoginRequiredMixin, TemplateView):
    template_name = 'AdminLte/brand/list.html'

    # for post request in delete
    @method_decorator(permission_required('products.delete_brand', raise_exception=True), name='dispatch')
    def post(self, request):
        multi_delete(request, Brand)
        return redirect('products:brand_list')


@method_decorator(permission_required('products.view_brand', raise_exception=True), name='dispatch')
class BrandListJson(LoginRequiredMixin, BaseDatatableView):
    columns = ['id', 'name', 'name_ar', 'description', 'description_ar', 'image']
    order_columns = ['id', 'name', 'name_ar', 'description', 'description_ar', 'image']
    max_display_length = 30
    model = Brand

    def render_column(self, row, column):
        if column == 'image':
            return str(row.image.url)
        else:
            return super().render_column(row, column)

    def get_initial_queryset(self):
        return Brand.objects.all().order_by('-created_at')

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(name_ar__icontains=search) |
                Q(description__icontains=search) |
                Q(description_ar__icontains=search)
            )
        return qs


@method_decorator(permission_required('products.view_brand', raise_exception=True), name='dispatch')
class BrandDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'brand'
    model = Brand
    template_name = 'AdminLte/brand/detail.html'


@method_decorator(permission_required('products.add_brand', raise_exception=True), name='dispatch')
class BrandCreateView(LoginRequiredMixin, CreateView):
    fields = ('name', 'name_ar', 'description', 'description_ar', 'image')
    model = Brand
    template_name = 'AdminLte/brand/form.html'

    # to edit form fields that class generate
    def get_form(self, form_class=None):
        form = super(BrandCreateView, self).get_form()
        form.fields['description'] = forms.CharField(widget=forms.Textarea)
        form.fields['description_ar'] = forms.CharField(widget=forms.Textarea)
        # overwrite template name of image filed widget to customize design
        form.fields['image'].widget.template_name = 'AdminLte/clearable_file_input.html'
        return form

    def get_success_url(self):
        if self.request.POST.get('another', None):
            return reverse_lazy('products:brand_add')
        return reverse_lazy('products:brand_detail', kwargs={'pk': self.object.pk})


@method_decorator(permission_required('products.change_brand', raise_exception=True), name='dispatch')
class BrandUpdateView(LoginRequiredMixin, UpdateView):
    fields = ('name', 'name_ar', 'description', 'description_ar', 'image')
    model = Brand
    template_name = 'AdminLte/brand/form.html'

    # to edit form fields that class generate
    def get_form(self, form_class=None):
        form = super(BrandUpdateView, self).get_form()
        form.fields['description'] = forms.CharField(widget=forms.Textarea)
        form.fields['description_ar'] = forms.CharField(widget=forms.Textarea)
        # overwrite template name of image filed widget to customize design
        form.fields['image'].widget.template_name = 'AdminLte/clearable_file_input.html'
        return form

    def get_success_url(self):
        return reverse_lazy('products:brand_detail', kwargs={'pk': self.object.pk})


@method_decorator(permission_required('products.delete_brand', raise_exception=True), name='dispatch')
class BrandDeleteView(LoginRequiredMixin, DeleteView):
    model = Brand
    success_url = reverse_lazy('products:brand_list')
    template_name = 'AdminLte/brand/delete.html'


# Product Views
@method_decorator(permission_required('products.view_product', raise_exception=True), name='dispatch')
class ProductListView(LoginRequiredMixin, TemplateView):
    template_name = 'AdminLte/product/list.html'

    # for post request in delete
    @method_decorator(permission_required('products.delete_product', raise_exception=True), name='dispatch')
    def post(self, request):
        multi_delete(request, Product)
        return redirect('products:product_list')


@method_decorator(permission_required('products.view_product', raise_exception=True), name='dispatch')
class ProductListJson(LoginRequiredMixin, BaseDatatableView):
    columns = ['id', 'name', 'name_ar', 'description', 'description_ar', 'sku', 'price', 'weight', 'stock',
               'main_image']
    order_columns = ['id', 'name', 'name_ar', 'description', 'description_ar', 'sku', 'price', 'weight', 'stock',
                     'main_image']
    max_display_length = 30
    model = Product

    def render_column(self, row, column):
        if column == 'main_image':
            return str(row.main_image.url)
        else:
            return super().render_column(row, column)

    def get_initial_queryset(self):
        return Product.objects.all().order_by('-created_at')

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(name_ar__icontains=search) |
                Q(description__icontains=search) |
                Q(description_ar__icontains=search) |
                Q(sku__icontains=search) |
                Q(price__icontains=search) |
                Q(weight__icontains=search) |
                Q(stock__icontains=search)
            )
        return qs


@method_decorator(permission_required('products.view_product', raise_exception=True), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'product'
    model = Product
    template_name = 'AdminLte/product/detail.html'


@method_decorator(permission_required('products.add_product', raise_exception=True), name='dispatch')
class ProductCreateView(LoginRequiredMixin, CreateView):
    fields = (
        'name', 'name_ar', 'description', 'description_ar', 'sku', 'price', 'weight', 'stock', 'main_image',
        'categories', 'options', 'brand', 'show')
    model = Product
    template_name = 'AdminLte/product/form.html'

    # to edit form fields that class generate
    def get_form(self, form_class=None):
        form = super(ProductCreateView, self).get_form()
        form.fields['description'] = forms.CharField(widget=forms.Textarea)
        form.fields['description_ar'] = forms.CharField(widget=forms.Textarea)
        # overwrite template name of image filed widget to customize design
        form.fields['main_image'].widget.template_name = 'AdminLte/clearable_file_input.html'
        return form

    def post(self, request, *args, **kwargs):
        temp = super(ProductCreateView, self).post(request, *args, **kwargs)
        if self.object is None:
            return temp
        for img in request.FILES.getlist('images'):
            image = ProductImages(product_id=self.object, image=img)
            image.save()

        return redirect(self.get_success_url())

    def get_success_url(self):
        if self.request.POST.get('another', None):
            return reverse_lazy('products:product_add')
        return reverse_lazy('products:product_list')


@method_decorator(permission_required('products.change_product', raise_exception=True), name='dispatch')
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    fields = (
        'name', 'name_ar', 'description', 'description_ar', 'sku', 'price', 'weight', 'stock', 'main_image',
        'categories', 'options', 'brand', 'show')
    model = Product
    template_name = 'AdminLte/product/form.html'

    def get_form(self, form_class=None):
        form = super(ProductUpdateView, self).get_form()
        form.fields['description'] = forms.CharField(widget=forms.Textarea)
        form.fields['description_ar'] = forms.CharField(widget=forms.Textarea)
        # overwrite template name of image filed widget to customize design
        form.fields['main_image'].widget.template_name = 'AdminLte/clearable_file_input.html'
        return form

    def get_success_url(self):
        return reverse_lazy('products:product_list')

    def post(self, request, *args, **kwargs):
        super(ProductUpdateView, self).post(request, *args, **kwargs)

        for img in request.FILES.getlist('images'):
            image = ProductImages(product_id=self.object, image=img)
            image.save()

        if request.POST.get('delImg', None):
            image_ids = request.POST.get('delImg', None).split(',')[:-1]
            for image_id in image_ids:
                image = ProductImages.objects.get(pk=image_id)
                image.delete()
        return redirect(self.get_success_url())


@method_decorator(permission_required('products.delete_product', raise_exception=True), name='dispatch')
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('products:product_list')
    template_name = 'AdminLte/product/delete.html'


# End Admin Dashboard Views


# Site Views
class ProductView(DetailView):
    context_object_name = 'product'
    model = Product
    template_name = 'product/detail.html'
    queryset = Product.view_object.all()

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        relate_products = Product.view_object.all().filter(categories__in=self.object.categories.all()).distinct(
            'pk').exclude(pk=self.object.pk)[:4]
        context.update({'relate_products': relate_products})
        return context


# Ajax View Response just json
def add_cart(request):
    product_id = request.GET.get('product_id', None)
    quantity = request.GET.get('quantity', None)
    product = Product.view_object.get(id=product_id)
    if product_id and quantity and product:
        # Add to cart in database if user is authenticated by user
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=request.user)[0]
        # Add to cart in database if user is not authenticated by session key
        else:
            if not request.session.exists(request.session.session_key):
                request.session.create()
            # print(request.session.session_key)
            cart = Cart.objects.get_or_create(session_key=request.session.session_key)[0]
        try:
            # because  cart and product_id is unique together and if add product more than one time just update
            # quantity
            CartProduct.objects.create(cart=cart, product_id=product_id,
                                       quantity=quantity)
        except:
            cart_product = CartProduct.objects.get(cart=cart, product_id=product_id)
            cart_product.quantity = quantity
            cart_product.save()
        cart_count = cart.products.count()
        data = {'cart_count': cart_count}
        return JsonResponse(data)
    return Http404('not found')


# Ajax View Response just json
def delete_cart(request):
    product_id = request.GET.get('product_id', None)
    product = Product.view_object.get(id=product_id)
    if product_id and product:
        # delete from cart in database
        try:
            if request.user.is_authenticated:
                cart = Cart.objects.get(user=request.user)
            else:
                cart = Cart.objects.get(session_key=request.session.session_key)
            cp = CartProduct.objects.get(cart=cart, product_id=product_id)
            cp.delete()
        except:
            return Http404('not found')
        cart_count = cart.products.count()
        data = {'cart_count': cart_count}
        return JsonResponse(data)
    return Http404('not found')


# Ajax View Response just json
def update_cart(request):
    cart_list = request.GET.get('cart_list', None)
    if cart_list:
        cart_list = json.dumps(cart_list)
        cart_list = eval(json.loads(cart_list))

        # update cart in database
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        else:
            if not request.session.exists(request.session.session_key):
                request.session.create()
            cart = Cart.objects.get(session_key=request.session.session_key)
        try:
            # because  cart and product_id is unique together and if add product more than one time just update
            # quantity
            for c in cart_list:
                cart_product = CartProduct.objects.get(cart=cart, product_id=c['product_id'])
                cart_product.quantity = c['quantity']
                cart_product.save()

        except:
            return Http404('not found')
        cart_count = cart.products.count()
        data = {'cart_count': cart_count}
        return JsonResponse(data)
    return Http404('not found')


# Ajax View Response just json
def add_wish(request):
    product_id = request.GET.get('product_id', None)
    product = Product.view_object.get(id=product_id)
    if product_id and product:
        massage = False
        # Add to WishList in database if user is authenticated
        if request.user.is_authenticated:
            wish = WishList.objects.get_or_create(user=request.user)[0]
        else:
            if not request.session.exists(request.session.session_key):
                request.session.create()
            wish = WishList.objects.get_or_create(session_key=request.session.session_key)[0]
        if product in wish.products.all():
            # to add product to wish list just one time
            massage = _('Product in wish list')
        else:
            wish.products.add(product)
        wish_count = wish.products.count()
        data = {'wish_count': wish_count, 'massage': massage}
        return JsonResponse(data)
    return Http404('not found')


class ShopView(ListView):
    model = Product
    template_name = 'product/shop.html'
    context_object_name = 'products'
    paginate_by = 12
    queryset = Product.view_object.all()

    def get_queryset(self):
        queryset = super(ShopView, self).get_queryset()
        category = self.request.GET.get('category', None)
        if category:
            queryset = queryset.filter(categories=category)
        return queryset


def cart_view(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(user=request.user)[0]
    else:
        cart = Cart.objects.get_or_create(session_key=request.session.session_key)[0]

    return render(request, 'product/cart.html', context={'cart': cart})

# End Site Views
