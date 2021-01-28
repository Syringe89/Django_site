from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import News
import re


class ContactForm(forms.Form):
    subject = forms.CharField(label='Тема', widget=forms.TextInput(attrs={"class": "form-control", }))
    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={"class": "form-control", 'rows': 5}))


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        "class": "form-control",
        'autocomplete': False
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        "class": "form-control",
        'autocomplete': 'off'
    }))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        "class": "form-control",
        'autocomplete': 'off'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = '__all__'
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'content': forms.Textarea(attrs={"class": "form-control", "rows": "5"}),
            'category': forms.Select(attrs={"class": "form-control"})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Заголовок не должен начинаться с цифры')
        return title

    """
    title = forms.CharField(max_length=150, label='Заголовок', widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(label='Контент', required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": "5",
    }))
    is_published = forms.BooleanField(label='Опубликовано', initial=True)
    category = forms.ModelChoiceField(Category.objects.all(), label='Категория', empty_label='Выберите категорию',
                                      widget=forms.Select(attrs={"class": "form-control"}))
    """
