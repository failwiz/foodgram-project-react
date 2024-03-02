import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Занесение в БД ингредиентов"

    def _import_ingredients(self):
        with open('initial_data/ingredients.csv') as ingredients:
            Ingredient.objects.bulk_create(
                [
                    Ingredient(**row) for row in csv.DictReader(
                        ingredients,
                        fieldnames=('name', 'measurement_unit'),
                    )
                ]
            )
        self.stdout.write('Ингредиенты занесены в БД')

    def handle(self, *args, **kwargs):
        self._import_ingredients()
