from django import forms
from .models import Teacher, Rating, UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, UserCreationForm


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    email = forms.EmailField(label='Электронная почта')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput
                                   (attrs={'autofocus': 'True'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)


# Форма для добавления и редактирования преподавателя
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'patronymic', 'department']


# Форма для добавления и редактирования рейтинга преподавателя
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'comment']
        widgets = {
            'score': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={
                'rows': 3, 'placeholder': 'Ваш отзыв'
            })
        }
        labels = {
            'score': 'Оценка (1-5)',
            'comment': 'Комментарий',
        }


# Форма для регистрации нового пользователя
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Обязательное поле. До 150 символов.'
        self.fields['password1'].help_text = 'Минимум 8 символов.'
        self.fields['password2'].help_text = 'Повторите пароль для подтверждения.'
