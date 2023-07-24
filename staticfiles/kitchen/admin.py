from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from kitchen.models import Category, Dish, Cook

admin.site.unregister(Group)

admin.site.register(Category)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price"]


@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("year_of_experience",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("year_of_experience", "photo")}),)
    )
