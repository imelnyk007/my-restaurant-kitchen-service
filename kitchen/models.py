from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=63)


class Cook(AbstractUser):
    year_of_experience = models.IntegerField()
    photo = models.ImageField(null=True, blank=True, upload_to="cook_photo/")

    class Meta:
        verbose_name = "cook"
        verbose_name_plural = "cooks"


class Dish(models.Model):
    name = models.CharField(max_length=63)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cooks = models.ManyToManyField(Cook, related_name="dishes")
    picture = models.ImageField(null=True, blank=True, upload_to="dish_pictures/")
