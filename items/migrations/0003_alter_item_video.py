# Generated by Django 5.0.4 on 2024-04-29 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_auto_20240427_0303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='video',
            field=models.FilePathField(blank=True, null=True, path='item_videos/'),
        ),
    ]
