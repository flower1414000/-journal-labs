from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from .forms import AttendanceForm, RegisterForm
from .models import Attendance, Student


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
                name=user.get_full_name() or user.username,
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
            return redirect('attendance_list')     # ← изменено
    else:
        form = AttendanceForm()

    return render(request, 'journal/add_attendance.html', {'form': form})


def attendance_list(request):
    records = Attendance.objects.select_related('student', 'student__group').all()
    return render(request, 'journal/attendance_list.html', {'records': records})