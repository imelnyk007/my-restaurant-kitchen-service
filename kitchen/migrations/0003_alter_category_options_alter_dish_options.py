# Generated by Django 4.2.3 on 2023-07-20 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0002_alter_cook_year_of_experience'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='dish',
            options={'verbose_name_plural': 'dishes'},
        ),
    ]
