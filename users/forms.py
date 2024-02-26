from django import forms
from users.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=150)
    email = forms.EmailField(max_length=256)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повторите пароль")
    # В Django то же, что и в html type="password"

    # Методы для валидации полей называются: `clean_` + `название поля`
    # Т.е. нет "опасных символов" и данные приведены в нужный формат
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким username уже существует')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():  # '.exist' равнозначно '.count() > 0'
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email

    # Общая проверка после проверки всех полей.
    def clean(self):
        data = self.cleaned_data
        if data["password1"] != data["password2"]:
            raise forms.ValidationError("Пароли не совпадают!")
        return data
