from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Пользователь электронного журнала."""

    @property
    def is_student(self):
        """True, если у пользователя есть профиль Student."""
        return hasattr(self, 'student_profile')

    @property
    def is_teacher(self):
        """True, если у пользователя есть профиль Teacher."""
        return hasattr(self, 'teacher_profile')

    def __str__(self):
        return self.get_full_name() or self.username

class Group(models.Model):
    name = models.CharField('Название группы', max_length=50)
    course = models.PositiveSmallIntegerField('Курс', null=True, blank=True)

    def __str__(self):
        return self.name

    def student_count(self):
        return self.student_set.count()

class Student(models.Model):
    name = models.CharField('ФИО студента', max_length=100)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name='Группа',
    )
    user_profile = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_profile',
        verbose_name='Учётная запись',
    )
    birth_date = models.DateField('Дата рождения', null=True, blank=True)

    def __str__(self):
        return f'{self.name} ({self.group.name})'


class Teacher(models.Model):
    name = models.CharField('ФИО преподавателя', max_length=100)
    user_profile = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teacher_profile',
        verbose_name='Учётная запись',
    )
    degree = models.CharField('Учёная степень', max_length=100, blank=True)
    department = models.CharField('Кафедра', max_length=100, blank=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name='Студент',
    )
    date = models.DateField('Дата занятия')
    present = models.BooleanField('Присутствовал', default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'date'],
                name='unique_student_attendance_date',
            ),
        ]
        verbose_name = 'Посещаемость'
        verbose_name_plural = 'Посещаемость'

    def __str__(self):
        status = 'Присутствовал' if self.present else 'Отсутствовал'
        return f'{self.student.name} - {self.date}: {status}'