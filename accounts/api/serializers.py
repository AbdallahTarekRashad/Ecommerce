from django.contrib.auth.forms import SetPasswordForm
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    new_password1 = serializers.CharField(max_length=128, write_only=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'birth_date', 'new_password1', 'new_password2', 'phone', 'image']
        extra_kwargs = {'image': {'required': True}}

    def validate(self, attrs):
        password = attrs.get('new_password1', None)
        if password is None:
            return attrs
        set_password_form = SetPasswordForm(user=self, data=attrs)
        if not set_password_form.is_valid():
            raise serializers.ValidationError(set_password_form.errors)
        return attrs

    def create(self, validated_data):
        validated_data.pop('new_password1')
        new_password2 = validated_data.pop('new_password2')
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(new_password2)
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop('new_password1', None)
        validated_data.pop('new_password2', None)
        return super(UserSerializer, self).update(instance, validated_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserLoginDataSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, user):
        token = Token.objects.get_or_create(user=user)[0]
        return token.key

    class Meta:
        model = User
        fields = ['token', 'id', 'username']
