from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy, include
from .views import SignUpView, home, login_view, admin_home, SiteInfoUpdateView, AccountListView, AccountListJson, \
    AccountCreateView, AccountUpdateView, test, AccountDeleteView, CountryListView, CountryListJson, CountryCreateView, \
    CountryUpdateView, CountryDeleteView
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include('accounts.api.urls', namespace='accounts_api')),
    # -------------------------------------------------------------------------------------------
    # Forget Password
    # -------------------------------------------------------------------------------------------
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/reset_password.html',
             subject_template_name='accounts/password_reset_subject.txt',
             email_template_name='accounts/password_reset_email.html',
             success_url=reverse_lazy('accounts:password_reset_done')
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url=reverse_lazy('accounts:login')
         ),
         name='password_reset_confirm'),
    # Home Dirs
    path('', home, name='home'),

    path('test', test, name='test'),

    # Admin Dashboard Urls

    path('seller/', admin_home, name='admin_home'),
    path('seller/site_info', SiteInfoUpdateView.as_view(), name='site_info'),


    # Accounts Admin Dashboard Urls
    path('seller/account/', AccountListView.as_view(), name='account_list'),
    path('seller/account/data', AccountListJson.as_view(), name='account_list_data'),
    path('seller/account/add', AccountCreateView.as_view(), name='account_add'),
    path('seller/account/update/<int:pk>', AccountUpdateView.as_view(), name='account_update'),
    path('seller/account/delete/<int:pk>', AccountDeleteView.as_view(), name='account_delete'),

    # Accounts Admin Dashboard Urls
    path('seller/country/', CountryListView.as_view(), name='country_list'),
    path('seller/country/data', CountryListJson.as_view(), name='country_list_data'),
    path('seller/country/add', CountryCreateView.as_view(), name='country_add'),
    path('seller/country/update/<int:pk>', CountryUpdateView.as_view(), name='country_update'),
    path('seller/country/delete/<int:pk>', CountryDeleteView.as_view(), name='country_delete'),

]
