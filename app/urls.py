from django.urls import path

from . import views

# /recipe/

urlpatterns = [
    path('createingredient/', views.create_ingredient, name='create_ingredient'),
    path('create/', views.create_recipe, name='create-recipe'),
    path('update/<int:recipe_id>', views.update_recipe, name='update-recipe'),
    path('<int:recipe_id>', views.show_recipe, name='show-recipe'),
    path("favorites", views.ListFavoriteRecipesView.as_view(), name='show-favorite-recipes'),
    path("favorite/<int:recipe_id>", views.MakeFavoriteView.as_view(), name='make-favorite-recipe')
]
