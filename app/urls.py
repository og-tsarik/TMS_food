from django.urls import path

from .views import create_ingredient, create_recipe, show_recipe, update_recipe

# /recipe/

urlpatterns = [
    path('createingredient/', create_ingredient, name='create_ingredient'),
    path('create/', create_recipe, name='create-recipe'),
    path('update/<int:recipe_id>', update_recipe, name='update-recipe'),
    path('<int:recipe_id>', show_recipe, name='show-recipe'),
]
