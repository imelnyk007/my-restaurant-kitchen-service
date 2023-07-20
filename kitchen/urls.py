from django.urls import path

from kitchen.views import (
    index,
    CategoryListView,
    CategoryCreateView,
    DishListView,
    DishDetailView,
    CookListView,
    CookDetailView,
)

urlpatterns = [
    path("", index, name="index"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/create/", CategoryCreateView.as_view(), name="category-create"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),

]

app_name = "kitchen"
