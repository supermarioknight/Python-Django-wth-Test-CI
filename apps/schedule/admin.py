from django.contrib import admin
from .models import Teacher, Subject, Class, Student, Schedule

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Admin view for Teacher model."""
    list_display = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Admin view for Subject model."""
    list_display = ('name', 'teacher')


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    """Admin view for Class model."""
    list_display = ('name',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin view for Student model."""
    list_display = ('name', 'class_assigned')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    """Admin view for Schedule model."""
    list_display = ('class_assigned', 'subject', 'day_of_week', 'hour')
