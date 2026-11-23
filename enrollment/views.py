from .forms import StudentRegistrationForm
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StudentProfile


def login_view(request):
    """Authenticates a student using their Student ID and password."""
    if request.user.is_authenticated:
        return redirect('enrollment:dashboard')

    if request.method == "POST":
        student_id_input = request.POST.get("student_id", "").strip().upper()
        password = request.POST.get("password", "")

        profile = StudentProfile.objects.filter(student_id=student_id_input).select_related('user').first()
        if not profile:
            messages.error(request, f"Student ID '{student_id_input}' is not registered.")
            return render(request, "enrollment/login.html")

        user = authenticate(request, username=profile.user.username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {profile.first_name}!")
            return redirect('enrollment:dashboard')
        else:
            messages.error(request, "Incorrect password. Please try again.")

    return render(request, "enrollment/login.html")


def register_view(request):
    """Registers a new student account and creates their StudentProfile."""
    if request.user.is_authenticated:
        return redirect('enrollment:dashboard')

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now sign in with your Student ID.")
            return redirect('enrollment:login')
        else:
            messages.error(request, "Please correct the validation errors below.")
    else:
        form = StudentRegistrationForm()

    return render(request, "enrollment/register.html", {"form": form})


def logout_view(request):
    """Logs out the active user and redirects to the login page."""
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect('enrollment:login')


@login_required(login_url='enrollment:login')
def dashboard_view(request):
    """Displays the authenticated student's enrollment dashboard."""
    student = getattr(request.user, 'student_profile', None)
    return render(request, "enrollment/dashboard.html", {"student": student})

def student_list_view(request):
    """Displays all StudentProfile records in a searchable class directory."""
    query = request.GET.get('q', '').strip()
    students = StudentProfile.objects.select_related('user').all()

    if query:
        students = students.filter(
            Q(student_id__icontains=query) |
            Q(first_name__icontains=query) |
            Q(middle_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(course__icontains=query) |
            Q(year_level__icontains=query) |
            Q(section__icontains=query) |
            Q(email__icontains=query)
        )

    return render(request, 'enrollment/student_list.html', {
        'students': students,
        'query': query,
        'total_count': students.count(),
    })


def student_detail_view(request, pk):
    """Displays a specific student's Personal Info and Academic/Background Info."""
    student = get_object_or_404(StudentProfile.objects.select_related('user'), pk=pk)
    return render(request, 'enrollment/student_detail.html', {
        'student': student,
    })