# Generated by Django 5.1.1 on 2024-09-16 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='image_src',
            field=models.CharField(default='', max_length=200),
        ),
    ]
