from rest_framework import pagination
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscription
from api.serializers import SubscribeSerializer

User = get_user_model()


class LimitPageNumberPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'


class UserViewSet(UserViewSet): 
    pagination_class = LimitPageNumberPagination

    @action(detail=True, methods=('post',),
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id=None):
        user = request.user 
        author = get_object_or_404(User, id=id)

        if user == author:
            return Response({
                'errors': 'Вы не можете подписываться на самого себя.'
            }, status=status.HTTP_400_BAD_REQUEST)
        if Subscription.objects.filter(user=user, author=author).exists():
            return Response({ 
                'errors': 'Вы уже подписаны на данного пользователя.'
            }, status=status.HTTP_400_BAD_REQUEST)

        follow = Subscription.objects.create(user=user, author=author)
        serializer = SubscribeSerializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        user = request.user 
        author = get_object_or_404(User, id=id)
        if user == author: 
            return Response({ 
                'errors': 'Вы не можете отписываться от самого себя.'
            }, status=status.HTTP_400_BAD_REQUEST)
        follow = Subscription.objects.filter(user=user, author=author)
        if follow.exists(): 
            follow.delete() 
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({ 
            'errors': 'Вы не подписаны на этого автора.'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=(IsAuthenticated,)) 
    def subscriptions(self, request):
        user = request.user
        queryset = Subscription.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True, 
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
