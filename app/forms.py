from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from ckeditor.fields import CKEditorWidget
from .models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):
    preview_image = forms.ImageField(required=True)

    class Meta:
        model = Recipe  # указываем модель, на которой будет основана 'RecipeForm'
        fields = ["name", "preview_image", "time_minutes", "category", "ingredients", "description"]
        widgets = {
            "description": CKEditorWidget(),
        }

    def save(self, commit=True):
        image: InMemoryUploadedFile = self.cleaned_data["preview_image"]

        image_folder_path = settings.MEDIA_ROOT / "images"
        image_folder_path.mkdir(parents=True, exist_ok=True)

        with (image_folder_path / image.name).open("bw") as image_file:
            image_file.write(image.read())
        self.instance.preview_image = f"images/{image.name}"
        return super().save(commit)


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "calories_count", "description"]
        widgets = {
            "description": CKEditorWidget(),
        }

    def ingredient_exist(self):
        name = self.cleaned_data.get('name')
        if name and Ingredient.objects.filter(name=name).exists():
            raise forms.ValidationError('Такой ингредиент уже существует')
        return name
