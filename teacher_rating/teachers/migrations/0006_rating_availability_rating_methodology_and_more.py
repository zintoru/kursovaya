# Generated by Django 5.1.3 on 2024-12-16 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0005_teacher_academic_degree_teacher_academic_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='availability',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=1, help_text='Оценка доступности преподавателя от 1 до 5'),
        ),
        migrations.AddField(
            model_name='rating',
            name='methodology',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=1, help_text='Оценка методологии преподавания от 1 до 5'),
        ),
        migrations.AddField(
            model_name='rating',
            name='teaching_quality',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=1, help_text='Оценка качества преподавания от 1 до 5'),
        ),
    ]
