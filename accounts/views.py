from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from accounts.forms import CustomUserCreationForm, UserChangeForm, CustomUserAdminCreationForm, UserAdminChangeForm
from accounts.models import SiteInfo, User, Country
from products.models import Category, Product
from products.views import multi_delete
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from arabic_reshaper import ArabicReshaper
from bidi.algorithm import get_display


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:home')
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:home')
        else:
            return super(SignUpView, self).get(request, *args, **kwargs)

    # overwrite form_valid function to login after save object
    def form_valid(self, form):
        response = super(SignUpView, self).form_valid(form)
        user = authenticate(username=self.object.email, password=self.object.password)
        login(self.request, self.object, 'django.contrib.auth.backends.ModelBackend')
        return response


def login_view(request):
    form = AuthenticationForm()
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            user = get_user_model().objects.filter(username=username).first()
            if user is not None:
                user = authenticate(username=user.email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.GET:
                    if request.GET.get('next', None):
                        return redirect(request.GET.get('next'))
                else:
                    return redirect('accounts:home')
        else:
            form = AuthenticationForm(data=request.POST)
    if request.user.is_authenticated:
        return redirect('accounts:home')
    return render(request, 'accounts/login.html', {'form': form})


def home(request):
    categories = Category.objects.all()[:11]
    products = Product.view_object.filter(categories__in=categories)[:12]
    latest_products = Product.view_object.all().order_by('created_at')[:18]
    context = {'products': products, 'latest_products': latest_products}
    return render(request, 'index.html', context=context)


def test(request):
    # this view for generate PDF file with Arabic context
    path = str(settings.BASE_DIR) + '/accounts/Cairo-Regular.ttf'
    template = get_template('accounts/test.html')
    html = template.render(context={'path': path})
    # reshape the text
    configuration = {
        'use_unshaped_instead_of_isolated': True
    }
    reshaper = ArabicReshaper(configuration=configuration)
    rehaped_text = reshaper.reshape(html)
    bidi_text = get_display(rehaped_text)

    file = open('test.pdf', "w+b")
    pisaStatus = pisa.CreatePDF(bidi_text, dest=file,
                                encoding='utf-8')
    file.seek(0)
    pdf = file.read()
    file.close()

    return HttpResponse(pdf, content_type='application/pdf')


def admin_home(request):
    return render(request, 'AdminLte/base.html')


# Admin Dashboard Views


def add_permissions(request, user):
    # Option Permission
    option_view = request.POST.get("option-view", None)
    option_add = request.POST.get("option-add", None)
    option_update = request.POST.get("option-change", None)
    option_delete = request.POST.get("option-delete", None)
    if option_view:
        permission = Permission.objects.get(name='Can view Option')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can view Option')
        user.user_permissions.remove(permission)
    if option_add:
        permission = Permission.objects.get(name='Can add Option')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can add Option')
        user.user_permissions.remove(permission)
    if option_update:
        permission = Permission.objects.get(name='Can change Option')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can change Option')
        user.user_permissions.remove(permission)
    if option_delete:
        permission = Permission.objects.get(name='Can delete Option')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can delete Option')
        user.user_permissions.remove(permission)
    # Category Permission
    category_view = request.POST.get("category-view", None)
    category_add = request.POST.get("category-add", None)
    category_update = request.POST.get("category-change", None)
    category_delete = request.POST.get("category-delete", None)
    if category_view:
        permission = Permission.objects.get(name='Can view Category')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can view Category')
        user.user_permissions.remove(permission)
    if category_add:
        permission = Permission.objects.get(name='Can add Category')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can add Category')
        user.user_permissions.remove(permission)
    if category_update:
        permission = Permission.objects.get(name='Can change Category')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can change Category')
        user.user_permissions.remove(permission)
    if category_delete:
        permission = Permission.objects.get(name='Can delete Category')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can delete Category')
        user.user_permissions.remove(permission)
    # Brand Permission
    brand_view = request.POST.get("brand-view", None)
    brand_add = request.POST.get("brand-add", None)
    brand_update = request.POST.get("brand-change", None)
    brand_delete = request.POST.get("brand-delete", None)
    if brand_view:
        permission = Permission.objects.get(name='Can view Brand')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can view Brand')
        user.user_permissions.remove(permission)
    if brand_add:
        permission = Permission.objects.get(name='Can add Brand')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can add Brand')
        user.user_permissions.remove(permission)
    if brand_update:
        permission = Permission.objects.get(name='Can change Brand')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can change Brand')
        user.user_permissions.remove(permission)
    if brand_delete:
        permission = Permission.objects.get(name='Can delete Brand')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can delete Brand')
        user.user_permissions.remove(permission)
    # Product Permission
    product_view = request.POST.get("product-view", None)
    product_add = request.POST.get("product-add", None)
    product_update = request.POST.get("product-change", None)
    product_delete = request.POST.get("product-delete", None)
    if product_view:
        permission = Permission.objects.get(name='Can view Product')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can view Product')
        user.user_permissions.remove(permission)
    if product_add:
        permission = Permission.objects.get(name='Can add Product')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can add Product')
        user.user_permissions.remove(permission)
    if product_update:
        permission = Permission.objects.get(name='Can change Product')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can change Product')
        user.user_permissions.remove(permission)
    if product_delete:
        permission = Permission.objects.get(name='Can delete Product')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can delete Product')
        user.user_permissions.remove(permission)
    # Account Permission
    account_view = request.POST.get("user-view", None)
    account_add = request.POST.get("user-add", None)
    account_update = request.POST.get("user-change", None)
    account_delete = request.POST.get("user-delete", None)
    if account_view:
        permission = Permission.objects.get(name='Can view User')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can view User')
        user.user_permissions.remove(permission)
    if account_add:
        permission = Permission.objects.get(name='Can add User')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can add User')
        user.user_permissions.remove(permission)
    if account_update:
        permission = Permission.objects.get(name='Can change User')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can change User')
        user.user_permissions.remove(permission)
    if account_delete:
        permission = Permission.objects.get(name='Can delete User')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can delete User')
        user.user_permissions.remove(permission)
    # Country Permission
    country_view = request.POST.get("country-view", None)
    country_add = request.POST.get("country-add", None)
    country_update = request.POST.get("country-change", None)
    country_delete = request.POST.get("country-delete", None)
    if country_view:
        permission = Permission.objects.get(name='Can view Country')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can view Country')
        user.user_permissions.remove(permission)
    if country_add:
        permission = Permission.objects.get(name='Can add Country')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can add Country')
        user.user_permissions.remove(permission)
    if country_update:
        permission = Permission.objects.get(name='Can change Country')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can change Country')
        user.user_permissions.remove(permission)
    if country_delete:
        permission = Permission.objects.get(name='Can delete Country')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can delete Country')
        user.user_permissions.remove(permission)
    # SiteInfo Permission
    siteinfo_update = request.POST.get("siteinfo-change", None)
    if siteinfo_update:
        permission = Permission.objects.get(name='Can change Site Info')
        user.user_permissions.add(permission)
    else:
        permission = Permission.objects.get(name='Can change Site Info')
        user.user_permissions.remove(permission)

    return user


# Site Info Update View
@method_decorator(permission_required('accounts.change_siteinfo', raise_exception=True), name='dispatch')
class SiteInfoUpdateView(LoginRequiredMixin, UpdateView):
    fields = (
        'name', 'name_ar', 'address', 'address_ar', 'email', 'phone', 'phone2', 'facebook', 'twitter', 'instagram',
        'linkedin', 'logo', 'whatsapp_btn')
    model = SiteInfo
    template_name = 'AdminLte/site_info/form.html'

    def get_object(self, queryset=None):
        return SiteInfo.objects.all().first()

    def get_form(self, form_class=None):
        form = super(SiteInfoUpdateView, self).get_form()
        # overwrite template name of image filed widget to customize design
        form.fields['logo'].widget.template_name = 'AdminLte/clearable_file_input.html'
        return form

    def get_success_url(self):
        return reverse_lazy('accounts:site_info')


# Admin Account Views
@method_decorator(permission_required('accounts.view_user', raise_exception=True), name='dispatch')
class AccountListView(LoginRequiredMixin, TemplateView):
    template_name = 'AdminLte/account/list.html'

    # for post request in delete
    @method_decorator(permission_required('accounts.delete_user', raise_exception=True))
    def post(self, request):
        multi_delete(request, User)
        return redirect('accounts:account_list')


@method_decorator(permission_required('accounts.view_user', raise_exception=True), name='dispatch')
class AccountListJson(LoginRequiredMixin, BaseDatatableView):
    columns = ['id', 'username', 'email', 'full_name', 'birth_date', 'is_active', 'image']
    order_columns = ['id', 'username', 'email', 'full_name', 'birth_date', 'is_active', 'image']
    max_display_length = 30
    model = User

    def render_column(self, row, column):
        if column == 'image':
            if row.image:
                return str(row.image.url)
            else:
                return 'https://st2.depositphotos.com/4520249/7735/v/950/depositphotos_77356830-stock-illustration' \
                       '-user-character-icon.jpg '
        elif column == 'full_name':
            return str(row.get_full_name())
        else:
            return super().render_column(row, column)

    def get_initial_queryset(self):
        return User.objects.filter(type=1)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        is_active = self.request.GET.get('columns[6][search][value]', None)
        if not is_active:
            is_active = self.request.GET.get('columns[5][search][value]', None)
        if search:
            qs = qs.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(birth_date__icontains=search)
            )
        if is_active:
            qs = qs.filter(is_active=is_active)
        return qs


@method_decorator(permission_required('accounts.add_user', raise_exception=True), name='dispatch')
class AccountCreateView(LoginRequiredMixin, CreateView):
    model = User
    template_name = 'AdminLte/account/form.html'
    form_class = CustomUserAdminCreationForm

    # to edit form fields that class generate
    def get_form(self, form_class=None):
        form = super(AccountCreateView, self).get_form()
        # another solution but i not used
        # form.fields['user_permissions'].queryset = Permission.objects.filter(Q(content_type__model='user') |
        #                                                                      Q(content_type__model='category') |
        #                                                                      Q(content_type__model='option') |
        #                                                                      Q(content_type__model='product') |
        #                                                                      Q(name__contains='Can change Site Info'))

        # overwrite template name of image filed widget to customize design
        form.fields['image'].widget.template_name = 'AdminLte/clearable_file_input.html'
        return form

    def post(self, request, *args, **kwargs):
        temp = super(AccountCreateView, self).post(request, *args, **kwargs)
        if self.object is None:
            return temp
        user = add_permissions(request, self.object)
        user.type = 1
        user.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        if self.request.POST.get('another', None):
            return reverse_lazy('accounts:account_add')
        return reverse_lazy('accounts:account_list')


@method_decorator(permission_required('accounts.change_user', raise_exception=True), name='dispatch')
class AccountUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserAdminChangeForm
    model = User
    template_name = 'AdminLte/account/form.html'
    context_object_name = 'account'

    def get_form(self, form_class=None):
        form = super(AccountUpdateView, self).get_form()
        # overwrite template name of image filed widget to customize design
        form.fields['image'].widget.template_name = 'AdminLte/clearable_file_input.html'
        return form

    def get_object(self, queryset=None):
        obj = super(AccountUpdateView, self).get_object(queryset=None)
        if obj.type == 1:
            return obj
        else:
            raise Http404("No User With This Id")

    def get_success_url(self):
        return reverse_lazy('accounts:account_list')

    def post(self, request, *args, **kwargs):
        temp = super(AccountUpdateView, self).post(request, *args, **kwargs)
        if self.object is None:
            return temp
        user = add_permissions(request, self.object)
        user.save()
        return redirect(self.get_success_url())


@method_decorator(permission_required('accounts.delete_user', raise_exception=True), name='dispatch')
class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    context_object_name = 'account'
    success_url = reverse_lazy('accounts:account_list')
    template_name = 'AdminLte/account/delete.html'


# Admin Country Views
@method_decorator(permission_required('accounts.view_country', raise_exception=True), name='dispatch')
class CountryListView(LoginRequiredMixin, TemplateView):
    template_name = 'AdminLte/country/list.html'

    # for post request in delete
    @method_decorator(permission_required('accounts.delete_country', raise_exception=True))
    def post(self, request):
        multi_delete(request, Country)
        return redirect('accounts:country_list')


@method_decorator(permission_required('accounts.view_country', raise_exception=True), name='dispatch')
class CountryListJson(LoginRequiredMixin, BaseDatatableView):
    columns = ['id', 'name_en', 'name_ar', 'logo']
    order_columns = ['id', 'name_en', 'name_ar', 'logo']
    max_display_length = 100
    model = Country

    def get_initial_queryset(self):
        return Country.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(name_ar__icontains=search) |
                Q(name_en__icontains=search) |
                Q(logo__icontains=search)
            )
        return qs


@method_decorator(permission_required('accounts.add_country', raise_exception=True), name='dispatch')
class CountryCreateView(LoginRequiredMixin, CreateView):
    model = Country
    template_name = 'AdminLte/country/form.html'
    fields = ['name_ar', 'name_en', 'logo']

    def get_success_url(self):
        if self.request.POST.get('another', None):
            return reverse_lazy('accounts:country_add')
        return reverse_lazy('accounts:country_list')


@method_decorator(permission_required('accounts.change_country', raise_exception=True), name='dispatch')
class CountryUpdateView(LoginRequiredMixin, UpdateView):
    model = Country
    fields = ['name_ar', 'name_en', 'logo']
    template_name = 'AdminLte/country/form.html'
    context_object_name = 'country'
    success_url = reverse_lazy('accounts:country_list')


@method_decorator(permission_required('accounts.delete_country', raise_exception=True), name='dispatch')
class CountryDeleteView(LoginRequiredMixin, DeleteView):
    model = Country
    context_object_name = 'country'
    success_url = reverse_lazy('accounts:country_list')
    template_name = 'AdminLte/country/delete.html'
