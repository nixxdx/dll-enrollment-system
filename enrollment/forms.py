import re
from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import StudentProfile

SECTION_CHOICES = [
    ('', '- Select Section -'),
    ('A', 'Section A'),
    ('B', 'Section B'),
    ('C', 'Section C'),
    ('D', 'Section D'),
]

COURSE_CHOICES = [
    ('', '- Select Course -'),
    ('ABELS', 'Bachelor of Arts in English Language Studies (ABELS)'),
    ('BSA', 'Bachelor of Science in Accountancy (BSA)'),
    ('BSAIS', 'Bachelor of Science in Accounting Information System (BSAIS)'),
    ('BSIT', 'Bachelor of Science in Information Technology (BSIT)'),
    ('BSE', 'Bachelor of Science in Entrepreneurship (BSE)'),
    ('BSPA', 'Bachelor of Science in Public Administration (BSPA)'),
    ('BSSW', 'Bachelor of Science in Social Work (BSSW)'),
    ('BTVTED', 'Bachelor of Technical Vocational Teachers Education (BTVTED)'),
    ('DHRS', 'Diploma in Hotel & Restaurant Services (DHRS)'),
]

YEAR_CHOICES = [
    ('', '- Select Year Level -'),
    ('1st Year', '1st Year'),
    ('2nd Year', '2nd Year'),
    ('3rd Year', '3rd Year'),
    ('4th Year', '4th Year'),
]


class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
        min_length=8
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )

    class Meta:
        model = StudentProfile
        fields = [
            'student_id', 'first_name', 'middle_name', 'last_name',
            'birthdate', 'age', 'contact_number', 'email', 'address',
            'course', 'year_level', 'section'
        ]
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '024A-00000'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name (Optional)'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'birthdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age', 'min': 15, 'max': 100}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '09123456789'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Barangay, Lucena City, Quezon'}),
            'course': forms.Select(choices=COURSE_CHOICES, attrs={'class': 'form-select'}),
            'year_level': forms.Select(choices=YEAR_CHOICES, attrs={'class': 'form-select'}),
            'section': forms.Select(choices=SECTION_CHOICES, attrs={'class': 'form-select'}),
        }

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id', '').strip().upper()
        if not re.match(r'^\d{3}[A-Z]-\d{5}$', student_id):
            raise ValidationError("Student ID format must strictly follow 024A-00000 pattern.")
        if StudentProfile.objects.filter(student_id=student_id).exists() or User.objects.filter(username=student_id).exists():
            raise ValidationError("A student with this ID already exists.")
        return student_id

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip().title()
        if len(first_name) < 2:
            raise ValidationError("First name must be at least 2 characters long.")
        if not re.match(r"^[A-Za-z\s'-]+$", first_name):
            raise ValidationError("First name can only contain letters, spaces, hyphens, and apostrophes.")
        return first_name

    def clean_middle_name(self):
        middle_name = self.cleaned_data.get('middle_name', '')
        if middle_name:
            middle_name = middle_name.strip().title()
            if not re.match(r"^[A-Za-z\s'-]+$", middle_name):
                raise ValidationError("Middle name can only contain letters, spaces, hyphens, and apostrophes.")
        return middle_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '').strip().title()
        if len(last_name) < 2:
            raise ValidationError("Last name must be at least 2 characters long.")
        if not re.match(r"^[A-Za-z\s'-]+$", last_name):
            raise ValidationError("Last name can only contain letters, spaces, hyphens, and apostrophes.")
        return last_name

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate and birthdate >= date.today():
            raise ValidationError("Birthdate cannot be in the future.")
        return birthdate

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is None or age < 15 or age > 100:
            raise ValidationError("Please provide a valid student age between 15 and 100.")
        return age

    def clean_contact_number(self):
        contact = self.cleaned_data.get('contact_number', '').strip().replace(' ', '').replace('-', '')
        if not re.match(r'^(09|\+639)\d{9}$', contact):
            raise ValidationError("Enter a valid PH mobile number (e.g., 09123456789).")
        return contact

    def clean_address(self):
        address = self.cleaned_data.get('address', '').strip()
        if len(address) < 5:
            raise ValidationError("Please enter your complete residential address.")
        return address

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email=email).exists() or StudentProfile.objects.filter(email=email).exists():
            raise ValidationError("An account with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match.")
            if len(password) < 8:
                self.add_error('password', "Password must be at least 8 characters long.")
            if not any(char.isdigit() for char in password):
                self.add_error('password', "Password must contain at least one digit.")
            if not any(char.isalpha() for char in password):
                self.add_error('password', "Password must contain at least one letter.")

        return cleaned_data

    def save(self, commit=True):
        student_profile = super().save(commit=False)
        student_id = self.cleaned_data['student_id']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        user = User.objects.create_user(
            username=student_id,
            email=email,
            password=password,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )

        student_profile.user = user
        if commit:
            student_profile.save()
        return student_profile