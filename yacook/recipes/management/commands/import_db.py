import csv
import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from transliterate import translit

from ...models import Group, Recipe


class Command(BaseCommand):
    help = 'Import data from csv file'

    def handle(self, *args, **options):
        data = os.path.join(settings.BASE_DIR, 'upload/all_recipes.csv')
        new_recipes = []
        with open(data, encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=",")
            for row in reader:
                title = row['title']
                description = '\n'.join(json.loads(row['description'].replace("'", '"')))
                ingredients_row = json.loads(row['ingredients'].replace("'", '"'))
                ingredients = '\n'.join([i + ':' + ' ' + ingredients_row[i] for i in ingredients_row])
                technology = '\n'.join(json.loads(row['technology'].replace("'", '"')))
                image = 'recipes/' + row['name'] + '.jpg'
                group_title = row['group']
                group_slug = translit(group_title, language_code='ru', reversed=True).lower().replace(' ', '_')
                group, _ = Group.objects.get_or_create(title=group_title, slug=group_slug)
                recipe = Recipe(
                    title=title,
                    description=description,
                    ingredients=ingredients,
                    technology=technology,
                    image=image,
                    author_id=1,
                    group=group
                )
                new_recipes.append(recipe)
        Recipe.objects.bulk_create(new_recipes)
