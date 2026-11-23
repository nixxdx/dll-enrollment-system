from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

student_id_validator = RegexValidator(
    regex=r'^\d{3}[A-Z]-\d{5}$',
    message="Student ID must strictly follow format '024A-00000' (3 digits, 1 uppercase letter, hyphen, 5 digits)."
)

name_validator = RegexValidator(
    regex=r"^[A-Za-z\s'-]+$",
    message="Name can only contain alphabetic characters, spaces, hyphens, and apostrophes."
)

contact_validator = RegexValidator(
    regex=r'^(09|\+639)\d{9}$',
    message="Contact number must be a valid Philippine mobile number (e.g., 09123456789)."
)


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=15, unique=True, validators=[student_id_validator])

    first_name = models.CharField(max_length=50, validators=[name_validator])
    middle_name = models.CharField(max_length=50, blank=True, null=True, validators=[name_validator])
    last_name = models.CharField(max_length=50, validators=[name_validator])

    birthdate = models.DateField()
    age = models.PositiveIntegerField(
        validators=[
            MinValueValidator(15, message="Age must be at least 15."),
            MaxValueValidator(100, message="Age cannot exceed 100.")
        ]
    )

    contact_number = models.CharField(max_length=15, validators=[contact_validator])
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)

    course = models.CharField(max_length=100)
    year_level = models.CharField(max_length=50)
    section = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.student_id})"