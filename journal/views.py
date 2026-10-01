from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from .forms import AttendanceForm, RegisterForm, StudentAvatarForm, StudentFilterForm
from .models import Attendance, Student
import os
import uuid
from pathlib import Path
from django.conf import settings
from django.http import HttpResponse




def index(request):
    context = {
        'welcome': 'Добро пожаловать в систему!',
        'menu': [
            {'url_name': 'home', 'title': 'Главная'},
            {'url_name': 'about', 'title': 'О системе'},
            {'url_name': 'contacts', 'title': 'Контакты'},
        ],
    }
    return render(request, 'journal/index.html', context)


def about(request):
    return render(request, 'journal/about.html')


def contacts(request):
    return render(request, 'journal/contacts.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(
                last_name=user.last_name or 'Фамилия',
                first_name=user.first_name or user.username,
                group=form.cleaned_data['group'],
                user_profile=user,
            )
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'journal/register.html', {'form': form})


def is_teacher(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_teacher)
def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm()

    return render(request, 'journal/add_attendance.html', {'form': form})


def attendance_list(request):
    records = Attendance.objects.select_related('student', 'student__group').all()
    return render(request, 'journal/attendance_list.html', {'records': records})




@login_required
def profile_dispatch(request):
    """
    Диспетчер по ролям: смотрит, кто пользователь, и перенаправляет
    на нужную страницу.
    Приоритет: студент → преподаватель → общая страница.
    """
    user = request.user
    if user.is_student:
        return redirect('student_page')
    elif user.is_teacher:
        return redirect('teacher_page')
    else:
        return render(request, 'journal/no_profile.html')


@login_required
def student_page(request):
    """Страница студента. Доступна только студентам."""
    if not request.user.is_student:
        return render(request, 'journal/no_access.html', {'title': 'Нет доступа'})
    return render(request, 'journal/student_page.html')


@login_required
def teacher_page(request):
    """Страница преподавателя. Доступна только преподавателям."""
    if not request.user.is_teacher:
        return render(request, 'journal/no_access.html', {'title': 'Нет доступа'})
<<<<<<< HEAD
    return render(request, 'journal/teacher_page.html')


def upload_raw(request):
    """Ручная загрузка файла через chunks() с уникальным именем."""
    if request.method == 'POST':
        uploaded = request.FILES.get('file_upload')
        if not uploaded:
            return render(request, 'journal/upload_raw.html', {
                'message': 'Файл не выбран. Пожалуйста, выберите файл.'
            })

        ext = os.path.splitext(uploaded.name)[1].lower()
        new_name = f"{uuid.uuid4().hex}{ext}"

        dest_dir = Path(settings.MEDIA_ROOT) / 'uploads'
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / new_name

        with dest.open('wb+') as out:
            for chunk in uploaded.chunks():
                out.write(chunk)

        return render(request, 'journal/upload_raw.html', {
            'message': f'Файл загружен: {new_name} (размер: {uploaded.size} байт)'
        })

    return render(request, 'journal/upload_raw.html')


@login_required
def student_avatar_update(request):
    """Обновление аватара студента."""
    u = request.user

    # Проверка: только авторизованный студент
    if not (u.is_authenticated and getattr(u, 'is_student', False)):
        return render(request, 'journal/no_access.html',
                      {'title': 'Нет доступа'}, status=403)

    student = u.student_profile

    if request.method == 'POST':
        form = StudentAvatarForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аватар обновлён')
            return redirect('profile_dispatch')
    else:
        form = StudentAvatarForm(instance=student)

    return render(request, 'journal/avatar_form.html', {'form': form})

def student_list(request):
    form = StudentFilterForm(request.GET or None)
    students = Student.objects.select_related('group').all()

    if form.is_valid():
        data = form.cleaned_data
        if data.get('last_name'):
            students = students.filter(last_name__icontains=data['last_name'])
        if data.get('group'):
            students = students.filter(group=data['group'])
        if data.get('group_name'):
            students = students.filter(group__name__icontains=data['group_name'])
    elif request.GET:
        students = Student.objects.none()  # некорректные параметры — пусто

    return render(request, 'journal/student_list.html', {
        'form': form, 'students': students,
    })
=======
    return render(request, 'journal/teacher_page.html')
>>>>>>> c7beefcafbab590e28882854e346ab22599d7a7e
