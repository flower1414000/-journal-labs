from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('accounts/register/', views.register, name='register'),
    path('attendance/add/', views.add_attendance, name='attendance_add'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    
    path('profile/', views.profile_dispatch, name='profile_dispatch'),
    path('student/', views.student_page, name='student_page'),
    path('teacher/', views.teacher_page, name='teacher_page'),
<<<<<<< HEAD
    path('upload/', views.upload_raw, name='upload_raw'),
    path('student/avatar/', views.student_avatar_update, name='student_avatar_update'),
    path('students/', views.student_list, name='student_list'),
=======
>>>>>>> c7beefcafbab590e28882854e346ab22599d7a7e
]