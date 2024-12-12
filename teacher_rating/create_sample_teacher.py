import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rating_system.settings')
django.setup()

from teachers.models import Teacher

# Create a sample teacher
teacher = Teacher.objects.create(
    first_name='Иван',
    last_name='Петров',
    patronymic='Сергеевич',
    department='Кафедра информатики',
    position='Доцент'
)

print(f'Created teacher: {teacher.first_name} {teacher.last_name} (ID: {teacher.id})')
