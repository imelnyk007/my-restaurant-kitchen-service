# Generated by Django 4.2.3 on 2023-07-21 16:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0005_alter_dish_options_alter_dish_cooks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='cooks',
            field=models.ManyToManyField(blank=True, null=True, related_name='dishes', to=settings.AUTH_USER_MODEL),
        ),
    ]
