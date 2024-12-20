from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.name


class Publication(models.Model):
    title = models.CharField(max_length=300)
    url = models.URLField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='publications/', blank=True, null=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='publications')

    def __str__(self):
        return self.title


class ThesisProject(models.Model):
    student_name = models.CharField(max_length=200)
    title = models.CharField(max_length=300)
    year = models.IntegerField()
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='thesis_projects')

    def __str__(self):
        return f"{self.student_name} - {self.title}"


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100, default='Преподаватель')
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    academic_degree = models.CharField(max_length=100, blank=True, null=True)
    academic_title = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.CharField(max_length=200, blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    experience_years = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='teacher_avatars/', null=True, blank=True)

    @property
    def avg_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            teaching_quality_avg = ratings.aggregate(Avg('teaching_quality'))['teaching_quality__avg'] or 0
            availability_avg = ratings.aggregate(Avg('availability'))['availability__avg'] or 0
            methodology_avg = ratings.aggregate(Avg('methodology'))['methodology__avg'] or 0
            
            # Вычисляем общий средний рейтинг по трем критериям
            total_ratings = teaching_quality_avg + availability_avg + methodology_avg
            count = sum(1 for x in [teaching_quality_avg, availability_avg, methodology_avg] if x > 0)
            return total_ratings / count if count > 0 else 0
        return 0

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Rating(models.Model):
    teacher = models.ForeignKey(
        'Teacher',
        # Можно использовать строку, если Teacher будет объявлена ниже
        related_name='ratings',
        # Это позволяет получить все рейтинги для преподавателя
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,  # Связь с пользователем
        on_delete=models.CASCADE
    )
    teaching_quality = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        help_text="Оценка качества преподавания от 1 до 5"
    )
    availability = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        help_text="Оценка доступности преподавателя от 1 до 5"
    )
    methodology = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        help_text="Оценка методологии преподавания от 1 до 5"
    )
    comment = models.TextField(
        blank=True, null=True,
        help_text="Комментарий к оценке (необязательно)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        # Это поле будет автоматически заполняться при создании записи
        help_text="Дата и время создания оценки"
    )

    class Meta:
        unique_together = ('teacher', 'user')
        # Каждый пользователь может оценить преподавателя только один раз
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"

    def __str__(self):
        return f'Рейтинг для {self.teacher}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='user_avatars/', null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a UserProfile when a new User is created
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Automatically save the UserProfile when the User is saved
    """
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
