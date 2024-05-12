from django.urls import include, path
from rest_framework import routers

from api.views import (IngredientsViewSet, RecipeViewSet,
                       TagsViewSet)
from users.views import UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]
