from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'enrollment'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Password Reset Flow (Connected to Gmail SMTP)
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='enrollment/reset_password.html',
            email_template_name='enrollment/password_reset_email.html',
            html_email_template_name='enrollment/password_reset_email.html',
            subject_template_name='enrollment/password_reset_subject.txt',
            success_url=reverse_lazy('enrollment:password_reset_done'),
        ),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='enrollment/reset_password_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='enrollment/reset_password_confirm.html',
            success_url=reverse_lazy('enrollment:password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='enrollment/reset_password_complete.html',
        ),
        name='password_reset_complete',
    ),
]