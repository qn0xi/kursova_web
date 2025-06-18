import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import FeedbackMessage

class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label='Ім\'я користувача')
    email = forms.EmailField(label='Електронна пошта')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Підтвердження пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if username.isdigit():
                raise forms.ValidationError("Ім'я користувача не може складатися лише з цифр.")
            if len(username) < 3:
                raise forms.ValidationError("Ім'я користувача має бути не менше 3 символів.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
            if not valid:
                raise forms.ValidationError("Будь ласка, введіть дійсну адресу електронної пошти.")
            
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Користувач з такою електронною поштою вже зареєстрований.")

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password) < 8:
                raise forms.ValidationError("Пароль має містити щонайменше 8 символів.")
            if not re.search(r'[A-Z]', password):
                raise forms.ValidationError("Пароль має містити хоча б одну велику літеру.")
            if not re.search(r'[a-z]', password):
                raise forms.ValidationError("Пароль має містити хоча б одну малу літеру.")
            if not re.search(r'\d', password):
                raise forms.ValidationError("Пароль має містити хоча б одну цифру.")
            if not re.search(r'[!@#$%^&*(),.?":{}|<>/\\]', password):
                raise forms.ValidationError("Пароль має містити хоча б один спеціальний символ.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError("Паролі не співпадають.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Ім\'я користувача')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedbackMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name', 'required': True}),
            'email': forms.EmailInput(attrs={'id': 'email', 'required': True}),
            'subject': forms.TextInput(attrs={'id': 'subject', 'required': True}),
            'message': forms.Textarea(attrs={'id': 'message', 'rows': 8, 'required': True}),
        } 