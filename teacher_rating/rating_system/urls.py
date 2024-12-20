from django.urls import path, include  # Импортируем необходимые модули
from django.contrib import admin
from django.contrib.auth import views as auth_views
from teachers import views  # Импортируем представления из приложения teachers
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Админ-панель Django
    path('admin/', admin.site.urls),

    # Стандартные URL для аутентификации (вход, выход, регистрация)
    path('accounts/', include('django.contrib.auth.urls')),  # Логин, выход

    # Страница входа
    path('login/', views.CustomLoginView.as_view(), name='login'),

    # Страница регистрации пользователя
    path('register/', views.register, name='register'),

    # Другие маршруты

    # Страница смены пароля
    path('password_change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),

    # Страница подтверждения смены пароля
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    # Страница сброса пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),

    # Страница подтверждения сброса пароля
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),

    # Страница ввода нового пароля по токену
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    # Страница завершения сброса пароля
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    # URL для преподавателей (все связанные страницы в приложении teachers)
    path('', include('teachers.urls')),  # Включаем URL-ы приложения teachers
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
