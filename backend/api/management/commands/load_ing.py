import csv

from django.core.management.base import BaseCommand

from api.models import Ingredient


class Command(BaseCommand):
    help = 'Загружает таблицу ингредиентов из csv-файла'

    def handle(self, *args, **options):
        ingredients = []
        with open('api/data/ingredients.csv', encoding='utf-8') as file:
            data_reader = csv.reader(file)
            for row in data_reader:
                name, unit = row
                ingredients.append(
                    Ingredient(name=name, measurement_unit=unit))

        Ingredient.objects.bulk_create(ingredients)

        self.stdout.write(self.style.SUCCESS('Ингредиенты загружены'))
