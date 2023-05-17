import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Импорт данных из ingredients.csv"

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Путь к файлу')

    def handle(self, *args, **options):
        if options['path'] is None:
            file_path = 'ingredients.csv'
        else:
            file_path = options['path'] + 'ingredients.csv'
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                try:
                    obj, created = Ingredient.objects.get_or_create(
                        name=row[0],
                        measurement_unit=row[1],
                    )
                    if not created:
                        self.stdout.write(
                            f'Ингредиент {obj} уже существует в базе данных')
                except Exception as error:
                    self.stdout.write(f'Ошибка в строке {row}: {error}')
