# Generated by Django 5.1.4 on 2025-01-21 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_meals_num_ratings_alter_meals_ratio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meals',
            name='num_ratings',
            field=models.IntegerField(default=0),
        ),
    ]
