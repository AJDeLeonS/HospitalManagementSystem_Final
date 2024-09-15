from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import PatientAccount, DoctorAccount, Appointment

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class PatientSignupForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')
    email = forms.EmailField(max_length=254, required=True, label='Email Address')
    phone_number = forms.CharField(max_length=15, required=True, label='Phone Number')
    class Meta:
        model = PatientAccount
        fields = ['phone_number', 'address', 'first_name', 'last_name', 'email']

class DoctorSignupForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')
    email = forms.EmailField(max_length=254, required=True, label='Email Address')
    phone_number = forms.CharField(max_length=15, required=True, label='Phone Number')
    class Meta:
        model = DoctorAccount
        fields = ['specialty', 'qualification', 'years_of_experience', 'first_name', 'last_name', 'email', 'phone_number']

class PatientLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class DoctorLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time', 'subject', 'description']

    doctor_choices = [
        ('dr_john_doe', 'Dr. John Doe'),
        ('dr_jane_smith', 'Dr. Jane Smith'),
        ('dr_rasheed_singh', 'Dr. Rasheed Singh'),
        ('dr_emily_davis', 'Dr. Emily Davis'),
    ]

    doctor = forms.ChoiceField(choices=doctor_choices)
