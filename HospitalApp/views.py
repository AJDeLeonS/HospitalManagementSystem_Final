from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import PatientSignupForm, DoctorSignupForm, PatientLoginForm, DoctorLoginForm, AppointmentForm
from .models import PatientAccount, DoctorAccount, Appointment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponseNotAllowed

def is_doctor(user):
    return hasattr(user, 'doctoraccount')

def is_patient(user):
    return hasattr(user, 'patientaccount')

@login_required
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    doctor_profile = DoctorAccount.objects.get(user=request.user)
    return render(request, 'DoctorsAccount/doctor_dashboard.html', {'doctor_profile': doctor_profile})

@login_required
@user_passes_test(is_patient)
def patient_dashboard(request):
    try:
        patient_profile = PatientAccount.objects.get(user=request.user)
    except PatientAccount.DoesNotExist:
        return redirect('home')
    return render(request, 'DoctorsAccount/patient_dashboard.html', {'user': request.user})

def home(request):
    return render(request, 'UserView/home.html')  # Or any other template you have for home

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        return HttpResponseNotAllowed(['POST'])

def signup(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            return redirect('home')
    else:
        user_form = UserCreationForm()
    return render(request, 'AccountView/signup.html', {'user_form': user_form})

def patient_signup(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        patient_form = PatientSignupForm(request.POST)

        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save()
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()
            login(request, user)
            return redirect('patient_dashboard')
    else:
        user_form = UserCreationForm()
        patient_form = PatientSignupForm()

    return render(request, 'AccountView/patient_signup.html', {
        'user_form': user_form,
        'patient_form': patient_form
    })

def doctor_signup(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        doctor_form = DoctorSignupForm(request.POST)

        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            login(request, user)
            return redirect('doctor_dashboard')
    else:
        user_form = UserCreationForm()
        doctor_form = DoctorSignupForm()

    return render(request, 'AccountView/doctor_signup.html', {
        'user_form': user_form,
        'doctor_form': doctor_form
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Handle invalid login
            pass
    return render(request, 'AccountView/login.html')

def patient_login(request):
    if request.method == 'POST':
        form = PatientLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if hasattr(user, 'patientaccount') and user.patientaccount.is_patient:
                    login(request, user)
                    return redirect('patient_dashboard')
                else:
                    form.add_error(None, 'User is not a patient')
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = PatientLoginForm()

    return render(request, 'AccountView/patient_login.html', {'form': form})

def doctor_login(request):
    if request.method == 'POST':
        form = DoctorLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if hasattr(user, 'doctoraccount') and user.doctoraccount.is_doctor:
                    login(request, user)
                    return redirect('doctor_dashboard')
                else:
                    messages.error(request, 'You are not registered as a doctor.')
            else:
                messages.error(request, 'Invalid username or password.')

            form = DoctorLoginForm()
    else:
        form = DoctorLoginForm()

    return render(request, 'AccountView/doctor_login.html', {'form': form})


def book_appointment_or_signup(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AppointmentForm(request.POST)
            if form.is_valid():
                appointment = form.save(commit=False)
                appointment.user = request.user
                appointment.save()

                # Optionally, print the form data
                doctor = form.cleaned_data['doctor']
                appointment_date = form.cleaned_data['appointment_date']
                appointment_time = form.cleaned_data['appointment_time']
                subject = form.cleaned_data['subject']
                description = form.cleaned_data['description']

                print(f"Doctor: {doctor}")
                print(f"Date: {appointment_date}")
                print(f"Time: {appointment_time}")
                print(f"Subject: {subject}")
                print(f"Description: {description}")

                # Redirect to home after booking
                return redirect('home')
        else:
            form = AppointmentForm()

        return render(request, 'UserView/appointment_page.html', {'form': form})
    else:
        return redirect('patient_signup')
