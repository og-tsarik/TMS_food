from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib.postgres.aggregates import ArrayAgg


from .favorite_service import FavoriteRecipesService
from .forms import RecipeForm, IngredientForm
from .models import Recipe, Ingredient


def home(request: WSGIRequest):
    recipes_queryset = (
        Recipe.objects.all()
        .prefetch_related("ingredients")
        .annotate(
            # Создание массива уникальных имен тегов для каждой заметки
            ingredients_list=ArrayAgg('ingredients__name', distinct=True)
        )
        .values("id", "name", "time_minutes", "preview_image", "ingredients_list", "category")
    )

    search = request.GET.get("search")
    if search:
        recipes_queryset = recipes_queryset.filter(description__search=search)

    print(recipes_queryset.query)

    return render(request, 'home.html', {"recipes": recipes_queryset})


@login_required  # Декоратор, который проверяет, зашел ли пользователь на сайт (не анонимный user)
def create_recipe(request: WSGIRequest):
    form = RecipeForm()

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)  # Файлы находятся отдельно!
        if form.is_valid():
            recipe: Recipe = form.save(commit=False)  # Не сохранять в базу рецепт, а вернуть его объект.
            # Так как нам необходимо и имя User'а
            recipe.user = request.user
            recipe.save()  # Сохраняем в базу объект.
            form.save_m2m()  # Сохраняем отношения many to many для ингредиентов и рецепта.

            return HttpResponseRedirect("/")

    return render(request, 'recipe-form.html', {'form': form})


@login_required  # Декоратор, который проверяет, зашел ли пользователь на сайт (не анонимный user)
def create_ingredient(request: WSGIRequest):
    form = IngredientForm()

    if request.method == 'POST':
        form = IngredientForm(request.POST)  # Файлы находятся отдельно!
        if form.is_valid():
            ingredient: Ingredient = form.save(commit=False)  # Не сохранять в базу рецепт, а вернуть его объект.
            # Так как нам необходимо и имя User'а
            ingredient.user = request.user
            ingredient.save()  # Сохраняем в базу объект.
            form.save_m2m()  # Сохраняем отношения many to many для ингредиентов и рецепта.

            return HttpResponseRedirect("/")

    return render(request, 'ingredient-create.html', {'form': form})


@login_required
def update_recipe(request: WSGIRequest, recipe_id: int):  # 'Добавляем recipe_id', т.к. обновляем конкретный рецепт
    recipe = get_object_or_404(Recipe, id=recipe_id)  # Указываем модель (Recipe) и какие поля искать (recipe_id)
    if recipe.user != request.user:
        return HttpResponseForbidden("You do not have permission to edit this recipe")

    form = RecipeForm(instance=recipe)  # 'instance' - показывает данные, которые уже есть

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)  # Файлы находятся отдельно!
        if form.is_valid():
            recipe: Recipe = form.save()  # Сохраняем (обновляем) в базу объект
            return HttpResponseRedirect(reverse("show-recipe", args=(recipe.id,)))

    return render(request, 'recipe-form.html', {'form': form})


def show_recipe(request: WSGIRequest, recipe_id: int):
    recipe: Recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, "recipe/recipe.html", {"recipe": recipe})


class ListFavoriteRecipesView(View):
    def get(self, request: WSGIRequest):
        """
        Метод `get` вызывается автоматический, когда HTTP метод запроса является `GET`.
        """
        favorite_service = FavoriteRecipesService(request)
        queryset = Recipe.objects.filter(id__in=favorite_service.favorites_ids)
        return render(request, "home.html", {"recipes": queryset})


class MakeFavoriteView(View):
    def post(self, request: WSGIRequest, recipe_id: int):
        """
        Метод `post` вызывается автоматический, когда HTTP метод запроса является `POST`.
        """
        recipe: Recipe = get_object_or_404(Recipe, id=recipe_id)
        self.make_favorite(request, recipe)
        return HttpResponseRedirect(reverse("show-recipe", args=(recipe.id,)))

    @staticmethod
    def make_favorite(request: WSGIRequest, recipe: Recipe):
        favorite_service = FavoriteRecipesService(request)
        if request.POST.get('favorite') == "no":
            favorite_service.remove_favorite(recipe.id)
        else:
            favorite_service.add_favorite(recipe)
