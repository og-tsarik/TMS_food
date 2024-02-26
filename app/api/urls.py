from django.urls import path

from . import views

# /api/recipes/

app_name = 'recipes:api'

urlpatterns = [
    # Классы представлений указываем через вызов метода `as_view`
    path("", views.RecipeListCreateAPIView.as_view(), name="recipes-list-create"),
    path("<int:pk>", views.DetailRecipeGenericAPIView.as_view(), name="recipe"),
]
