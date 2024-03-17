from django.core.handlers.wsgi import WSGIRequest

from .models import Recipe


class FavoriteRecipesService:

    def __init__(self, request: WSGIRequest):
        self._session = request.session

        # Если у сессии пользователя нет ключа `favorites`, то мы его создаем
        self._session.setdefault("favorites", [])

        # Если вдруг это был не список, то задаем его явно.
        if not isinstance(self._session["favorites"], list):
            self._session["favorites"] = []

    def add_favorite(self, recipe: Recipe) -> None:
        if recipe.id not in self._session["favorites"]:
            self._session["favorites"].append(recipe.id)
            self._session.save()  # Сохраняем в backend сессий

    def remove_favorite(self, recipe_id: int) -> None:
        try:
            self._session["favorites"].remove(recipe_id)
        except ValueError:
            pass
        else:
            self._session.save()  # Сохраняем в backend сессий

    @property
    def favorites_ids(self) -> list[int]:
        return self._session["favorites"]


def favorite_service_preprocessor(request: WSGIRequest) -> dict[str, list[int]]:
    return {"favorites_ids": FavoriteRecipesService(request).favorites_ids}
