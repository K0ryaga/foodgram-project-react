from django.contrib.admin import ModelAdmin, TabularInline, register, site
from django.utils.safestring import mark_safe

from .models import (Favorite, Ingredient, RecipeIngredient, Recipe,
                     ShoppingCart, Tag)

site.site_header = 'Администрирование Foodgram'


class RecipeIngredientInLine(TabularInline):
    model = RecipeIngredient
    min_num = 1
    extra = 1


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('id', 'name', 'author',
                    '_get_thumbnail', '_favorite_count')
    search_fields = ('name', 'author')
    list_filter = ('name', 'author__username')
    inlines = (RecipeIngredientInLine,)
    readonly_fields = ['_get_thumbnail']
    empty_value_display = '-пусто-'

    def _get_thumbnail(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" hieght="30" />')
    _get_thumbnail.short_description = 'Изображение'

    def _favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()
    _favorite_count.short_description = 'В Избранном'


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'


site.register(Favorite)
site.register(ShoppingCart)
