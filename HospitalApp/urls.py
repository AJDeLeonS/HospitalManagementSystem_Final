from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('patient_signup/', views.patient_signup, name='patient_signup'),
    path('doctor_signup/', views.doctor_signup, name='doctor_signup'),
    path('login/', views.login_view, name='login_view'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('logout/', views.logout_view, name='logout_view'),  # Your custom logout
    path('login/patient/', views.patient_login, name='patient_login'),
    path('login/doctor/', views.doctor_login, name='doctor_login'),
    path('book-appointment/', views.book_appointment_or_signup, name='book_appointment_or_signup'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
