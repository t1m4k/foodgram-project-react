import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Импорт данных из ingredients.csv"

    def handle(self, *args, **options):
        file_path = 'ingredients.csv'
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                try:
                    obj, created = Ingredient.objects.get_or_create(
                        name=row[0],
                        measurement_unit=row[1],
                    )
                    if not created:
                        print(f'Ингредиент {obj} уже существует в базе данных')
                except Exception as error:
                    print(f'Ошибка в строке {row}: {error}')
