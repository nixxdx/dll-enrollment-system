from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'last_name', 'first_name', 'middle_name', 'course', 'year_level', 'section', 'contact_number')
    search_fields = ('student_id', 'first_name', 'last_name', 'email')
    list_filter = ('course', 'year_level', 'section')