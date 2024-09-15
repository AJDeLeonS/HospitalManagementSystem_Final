from django.db import models
from django.contrib.auth.models import User


class PatientAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class DoctorAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    qualification = models.TextField(blank=True, null=True)
    years_of_experience = models.PositiveIntegerField()
    is_doctor = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

class Appointment(models.Model):
    doctor_choices = [
        ('dr_john_doe', 'Dr. John Doe'),
        ('dr_jane_smith', 'Dr. Jane Smith'),
        ('dr_rasheed_singh', 'Dr. Rasheed Singh'),
        ('dr_emily_davis', 'Dr. Emily Davis'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.CharField(max_length=50, choices=doctor_choices)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    subject = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.doctor} - {self.appointment_date}'
