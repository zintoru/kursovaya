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
    teaching_quality = forms.ChoiceField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        label='Качество преподавания'
    )
    availability = forms.ChoiceField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        label='Доступность'
    )
    methodology = forms.ChoiceField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        label='Методология'
    )

    class Meta:
        model = Rating
        fields = ['teaching_quality', 'availability', 'methodology', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш отзыв'})
        }
        labels = {
            'comment': 'Комментарий',
        }


# Форма для регистрации нового пользователя
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Электронная почта')
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Обязательное поле. До 150 символов.'
        self.fields['password1'].help_text = 'Минимум 8 символов.'
        self.fields['password2'].help_text = 'Повторите пароль для подтверждения.'
