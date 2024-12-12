# Generated by Django 5.1.3 on 2024-12-12 15:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0004_auto_20241212_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='academic_degree',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='academic_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='education',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='experience_years',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teacher',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='specialization',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='patronymic',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='teachers.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('url', models.URLField(blank=True, null=True)),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='publications/')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publications', to='teachers.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='ThesisProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=300)),
                ('year', models.IntegerField()),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thesis_projects', to='teachers.teacher')),
            ],
        ),
    ]
