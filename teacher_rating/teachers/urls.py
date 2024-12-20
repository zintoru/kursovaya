from django.urls import path
from . import views  # Импортируем представления из текущего приложения
from django.shortcuts import redirect
from .views import logout_view
from .views import CustomLoginView

urlpatterns = [
    # Перенаправление на главную
    path('accounts/profile/', lambda request: redirect('/')),

    # Страница профиля пользователя
    path('profile/', views.profile, name='profile'),

    # Страница редактирования профиля
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Страница смены пароля
    path('profile/change_password/', views.change_password,
         name='change_password'),

    # Страница со списком преподавателей
    path('', views.teacher_list, name='teacher_list'),

    # Детали преподавателя по его ID
    path('<int:teacher_id>/', views.teacher_detail, name='teacher_detail'),

    # Редактирование данных преподавателя
    path('edit/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),

    # Добавление отзыва (рейтинг) для преподавателя
    path('<int:teacher_id>/add_rating/', views.add_rating, name='add_rating'),

    # Редактирование отзыва
    path('edit_rating/<int:rating_id>/',
         views.edit_rating, name='edit_rating'),

    # Удаление отзыва
    path('delete_rating/<int:rating_id>/',
         views.delete_rating, name='delete_rating'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
