from django.contrib import admin
from .models import Teacher, Rating, UserProfile, Publication

class PublicationInline(admin.StackedInline):
    model = Publication
    extra = 1  # Количество пустых форм для добавления новых публикаций
    fields = ('title', 'url', 'pdf_file')

# Регистрация моделей в админ-панели
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'patronymic', 'department', 'position', 'avg_rating')
    list_filter = ('department', 'position')
    search_fields = ('last_name', 'first_name', 'patronymic', 'department')
    ordering = ('last_name', 'first_name')
    inlines = [PublicationInline]

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'teaching_quality', 'availability', 'methodology', 'average_rating_display')
    list_filter = ('teacher', 'created_at')
    search_fields = ('teacher__last_name', 'teacher__first_name', 'comment')
    date_hierarchy = 'created_at'

    def average_rating_display(self, obj):
        return (obj.teaching_quality + obj.availability + obj.methodology) / 3
    average_rating_display.short_description = 'Средняя оценка'

# Register UserProfile with admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)
