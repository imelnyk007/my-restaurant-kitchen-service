from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from kitchen.models import Dish, Cook


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Dish
        fields = "__all__"


class DishUpdateForm(forms.ModelForm):
    picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Dish
        fields = "__all__"


class CookCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "year_of_experience",
            "photo"
        )


class CookUpdateForm(forms.ModelForm):
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Cook
        fields = ['first_name', 'last_name', "year_of_experience", "photo"]


class CategoryNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"})
    )


class DishNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"})
    )


class CookUsernameSearchForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"})
    )
