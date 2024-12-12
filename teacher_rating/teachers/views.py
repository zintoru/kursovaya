from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import Group
from django.db.models import Avg
from .models import Teacher, Rating
from .forms import (TeacherForm, RatingForm, UserRegisterForm, UserProfileForm,
                    CustomPasswordChangeForm)


@login_required
def profile(request):
    # Профиль пользователя
    return render(request, 'teachers/profile.html')


@login_required
def edit_profile(request):
    # Редактирование данных профиля
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваши данные обновлены!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'teachers/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    # Смена пароля
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Сохраняем сессию
            messages.success(request, 'Ваш пароль был изменен!')
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'teachers/change_password.html', {'form': form})


# Функция для проверки прав администратора
def admin_required(user):
    return user.is_superuser


# Регистрация нового пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем форму
            messages.success(
                request, f'Аккаунт создан для {form.cleaned_data["username"]}'
            )
            return redirect('login')  # Перенаправление на страницу логина
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


# Редактирование рейтинга преподавателя
def edit_rating(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id)
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()  # Сохраняем измененную форму рейтинга
            return redirect('teacher_detail', teacher_id=rating.teacher.id)
    else:
        form = RatingForm(instance=rating)
    return render(request, 'teachers/edit_rating.html',
                  {'form': form, 'rating': rating})


# Удаление рейтинга преподавателя
def delete_rating(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id)
    teacher_id = rating.teacher.id
    rating.delete()  # Удаляем рейтинг
    return redirect('teacher_detail', teacher_id=teacher_id)


# Добавление нового рейтинга преподавателю
def add_rating(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    # Check if user has already rated this teacher
    existing_rating = Rating.objects.filter(teacher=teacher, user=request.user).first()
    
    if request.method == 'POST':
        if existing_rating:
            # If rating exists, update the existing rating
            form = RatingForm(request.POST, instance=existing_rating)
        else:
            # If no existing rating, create a new one
            form = RatingForm(request.POST)
        
        if form.is_valid():
            rating = form.save(commit=False)
            rating.teacher = teacher
            rating.user = request.user
            rating.save()
            messages.success(request, 'Ваш отзыв был успешно сохранен.')
            return redirect('teacher_detail', teacher_id=teacher.id)
    else:
        # If rating exists, pre-populate the form
        form = RatingForm(instance=existing_rating) if existing_rating else RatingForm()
    
    return render(request, 'teachers/add_rating.html', {
        'form': form, 
        'teacher': teacher,
        'existing_rating': existing_rating
    })


# Редактирование данных преподавателя
@user_passes_test(admin_required)
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()  # Сохраняем изменения в преподавателе
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'teachers/edit_teacher.html',
                  {'form': form, 'teacher': teacher})


# Список преподавателей с возможностью фильтрации и сортировки
@login_required
def teacher_list(request):
    query = request.GET.get('q', '')
    # Поиск по имени или фамилии
    sort_by = request.GET.get('sort_by', 'first_name')
    # Сортировка по умолчанию по имени
    teachers = Teacher.objects.annotate(
        avg_rating=Avg('ratings__score')
    )

    # Фильтрация по имени преподавателя
    if query:
        teachers = teachers.filter(
            first_name__icontains=query
        ) | teachers.filter(last_name__icontains=query)

    # Сортировка по рейтингу или имени
    if sort_by == 'rating':
        teachers = teachers.order_by('-avg_rating')
        # Сортировка по убыванию среднего рейтинга
    else:
        teachers = teachers.order_by(sort_by)
        # Сортировка по имени или фамилии

    return render(request, 'teachers/teacher_list.html',
                  {'teachers': teachers})


# Страница с деталями преподавателя и его рейтингами
@login_required
def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    ratings = teacher.ratings.all().order_by('-created_at')
    
    # Calculate average rating
    if ratings.exists():
        avg_rating = ratings.aggregate(Avg('score'))['score__avg']
    else:
        avg_rating = None
    
    # Get related data
    courses = teacher.courses.all()
    publications = teacher.publications.all()
    thesis_projects = teacher.thesis_projects.all().order_by('-year')
    
    # Ensure the view only handles GET requests for rendering the page
    if request.method == 'GET':
        return render(request, 'teachers/teacher_detail.html', {
            'teacher': teacher,
            'ratings': ratings,
            'avg_rating': avg_rating,
            'courses': courses,
            'publications': publications,
            'thesis_projects': thesis_projects,
        })
    else:
        return HttpResponseNotAllowed(['GET'])  # Return 405 for non-GET requests


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout
