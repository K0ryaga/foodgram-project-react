from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Subscription

User = get_user_model()


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (not user.is_anonymous
                and Subscription.objects.filter(
                    user=user,
                    author=obj.id).exists())


class UserCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email',
                  'password')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True},
            'email': {'required': True},
            'password': {'required': True},
        }
