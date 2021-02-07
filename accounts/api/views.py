from django.contrib.auth import authenticate, get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from accounts.api.serializers import UserSerializer, UserLoginDataSerializer, UserLoginSerializer


class UserRegisterView(CreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            return Response(
                data=UserLoginDataSerializer(serializer.save()).data
            )


class UserLoginAPIView(GenericAPIView):
    serializer_class = UserLoginSerializer
    authentication_classes = ()
    permission_classes = ()

    @swagger_auto_schema(operation_description="You can login with email or username", )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                user = get_user_model().objects.filter(username=username).first()
                if user is not None:
                    user = authenticate(username=user.email, password=password)
            if user is not None:
                if user.is_active:
                    return Response(
                        data=UserLoginDataSerializer(user).data, status=status.HTTP_200_OK
                    )
            raise AuthenticationFailed()

# class HomeTokenView(TemplateView):
#     template_name = 'api/test_social_auth.html'


# class BaseDetailView(generics.RetrieveAPIView):
#     permission_classes = IsAuthenticated,
#     serializer_class = UserSerializer
#     model = get_user_model()
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#
# class UserTokenDetailView(BaseDetailView):
#     authentication_classes = (TokenAuthentication,)
