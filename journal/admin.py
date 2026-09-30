from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Group, Student, Teacher, Attendance

admin.site.register(User, UserAdmin)
admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Attendance)
