# items/migrations/0006_add_initial_categories.py

from django.db import migrations

def add_initial_categories(apps, schema_editor):
    Category = apps.get_model('items', 'Category')
    initial_categories = [
        '전자기기',
        '가구',
        '의류',
        '스포츠용품',
        '책',
    ]
    for category_name in initial_categories:
        Category.objects.create(name=category_name)

class Migration(migrations.Migration):
    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_initial_categories),
    ]