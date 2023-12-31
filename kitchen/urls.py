from django.urls import path

from kitchen.views import (
    index,
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    DishListView,
    DishDetailView,
    CookListView,
    CookDetailView,
    update_dish,
    DishDeleteView,
    CookDeleteView,
    DishCreateView,
    toggle_assign_to_dish,
    register_request,
    update_cook,
    ChangePasswordView, CategoryDetailView, remove_cook_from_dish, remove_dish_from_cook,
)

urlpatterns = [
    path("", index, name="index"),
    path("register/", register_request, name="register"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/",
         CategoryDetailView.as_view(),
         name="category-detail"
         ),
    path("categories/create/",
         CategoryCreateView.as_view(),
         name="category-create"
         ),
    path("categories/<int:pk>/update/",
         CategoryUpdateView.as_view(),
         name="category-update"
         ),
    path("categories/<int:pk>/delete/",
         CategoryDeleteView.as_view(),
         name="category-delete"
         ),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path("dishes/<int:pk>/update/", update_dish, name="dish-update"),
    path("dishes/<int:pk>/delete/",
         DishDeleteView.as_view(),
         name="dish-delete"
         ),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("cooks/create/", register_request, name="cook-create"),
    path("cooks/<int:pk>/update/", update_cook, name="cook-update"),
    path("cooks/<int:pk>/change-password/",
         ChangePasswordView.as_view(),
         name="change-password"
         ),
    path("cooks/<int:pk>/delete/",
         CookDeleteView.as_view(),
         name="cook-delete"
         ),
    path("dishes/<int:pk>/toggle-assign/",
         toggle_assign_to_dish,
         name="toggle-dish-assign"
         ),
    path("dishes/<int:dish_id>/remove-cook/<int:cook_id>/",
         remove_cook_from_dish,
         name="remove_cook_from_dish"
         ),
    path("dishes/<int:cook_id>/remove-dish/<int:dish_id>/",
         remove_dish_from_cook,
         name="remove_dish_from_cook"
         ),
]

app_name = "kitchen"
