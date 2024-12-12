from django.contrib import admin
from django.contrib.auth.models import User
from .models import Teacher, Rating, UserProfile

# Регистрация моделей в админ-панели
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'patronymic', 'department', 'position', 'average_rating')
    list_filter = ('department', 'position')
    search_fields = ('last_name', 'first_name', 'patronymic', 'department')
    ordering = ('last_name', 'first_name')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'user', 'score', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('teacher__last_name', 'user__username')
    ordering = ('-created_at',)

# Register UserProfile with admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)
