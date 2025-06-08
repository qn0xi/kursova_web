from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Електронна пошта')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        labels = {
            'username': 'Ім\'я користувача',
            'password': 'Пароль',
            'password2': 'Підтвердження пароля',
        }
        help_texts = {
            'username': '',
            'password': '',
            'password2': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'email', 'password', 'password2']:
            if field_name in self.fields:
                self.fields[field_name].help_text = None

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'email',
            'password',
            'password2',
        )
        self.helper.add_input(Submit('submit', 'Зареєструватися'))


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Ім\'я користувача')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль') 