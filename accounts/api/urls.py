from django.urls import path, re_path, include
from rest_framework import permissions
from .views import UserRegisterView, UserLoginAPIView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth.decorators import user_passes_test

schema_view = get_schema_view(
    openapi.Info(
        title="Ecommerce API",
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)
app_name = 'accounts_api'
urlpatterns = [
    path('api/signup/', UserRegisterView.as_view(), name='api_signup'),
    path('api/login/', UserLoginAPIView.as_view(), name='api_login'),
    # under test
    path('api/login/', include('rest_social_auth.urls_token')),

    # Api Documentation

    path('api/doc/swagger/',
         user_passes_test(lambda u: u.is_superuser, )(schema_view.with_ui('swagger', cache_timeout=0)),
         name='api_swagger'),
    # path('api/doc/redoc/', user_passes_test(lambda u: u.is_superuser, )(schema_view.with_ui('redoc', cache_timeout=0)),
    #      name='api_redoc'),
    path('api/doc/redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='api_redoc'),
    # re_path(r'^api/doc/schema(?P<format>\.json|\.yaml)$',
    #         user_passes_test(lambda u: u.is_superuser, )(schema_view.without_ui(cache_timeout=0)),
    #         name='api_json_yaml'),
    re_path(r'^api/doc/schema(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
            name='api_json_yaml'),
]
