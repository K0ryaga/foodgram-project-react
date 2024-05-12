from rest_framework import pagination
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (RecipeCreateAndUpdateSerializer,
                          IngredientSerializer,
                          RecipeListSerializer,
                          ShortRecipeSerializer,
                          TagSerializer)
from .models import (Favorite,
                     Ingredient,
                     RecipeIngredient,
                     Recipe,
                     ShoppingCart,
                     Tag)

User = get_user_model()


class LimitPageNumberPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'


class TagsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if (self.action == 'list' or self.action == 'retrieve'):
            return RecipeListSerializer
        return RecipeCreateAndUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=(permissions.IsAuthenticated,))
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_recipe(Favorite, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_recipe(Favorite, request.user, pk)

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=(permissions.IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.add_recipe(ShoppingCart, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_recipe(ShoppingCart, request.user, pk)

    @action(detail=False, methods=('get',),
            permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request):
        user = request.user
        if not user.cart.exists():
            return Response({
                'errors': 'Ваш список покупок пуст.'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        ingredients = RecipeIngredient.objects.filter(
            recipe__cart__user=user).values(
                'ingredient__name',
                'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        filename = f'{user.username}_shopping_list.txt'
        shopping_list = (
            f'Список покупок({user.first_name})\n'
            f'{timezone.localtime().strftime("%d/%m/%Y %H:%M")}\n\n'
        )
        for ing in ingredients:
            shopping_list += (f'{ing["ingredient__name"]}: {ing["amount"]} '
                              f'{ing["ingredient__measurement_unit"]}\n')
        shopping_list += '\nFoodgram'
        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    def add_recipe(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({
                'errors': 'Рецепт уже добавлен в список.'
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Рецепт уже удален.'
        }, status=status.HTTP_400_BAD_REQUEST)
