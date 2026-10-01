from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Attendance, Group

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label='Группа',
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'group', 'password1', 'password2')


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('student', 'date', 'present')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from django.core.validators import FileExtensionValidator
from .models import Student

MAX_MB = 5


def validate_filesize(file):
    """Проверка размера файла ≤ 5 МБ."""
    if file.size > MAX_MB * 1024 * 1024:
        raise forms.ValidationError(f'Размер файла не должен превышать {MAX_MB} МБ')


class StudentAvatarForm(forms.ModelForm):
    """Форма для загрузки аватара студента."""

    class Meta:
        model = Student
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/png'}),
        }
        help_texts = {
            'avatar': 'Загрузите изображение (JPEG/PNG, до 5 МБ)',
        }

    avatar = forms.ImageField(
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_filesize,
        ],
        label='Аватар',
    )

class StudentFilterForm(forms.Form):
    """Форма фильтрации списка студентов (GET-параметры)."""
    last_name = forms.CharField(label='Часть фамилии', required=False)
    group = forms.ModelChoiceField(
        label='Группа',
        queryset=Group.objects.all(),
        required=False,
        empty_label='— все группы —',
    )
    group_name = forms.CharField(label='Часть названия группы', required=False)