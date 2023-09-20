from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='landing'),

    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),

    path('about/', views.about, name='about'),
    path('terms/', views.terms, name='terms'),
    path('privacy-policy/', views.privacy, name='privacy'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),

    path('specialities', views.specialityList, name='specialities'),
    path('specialities/<str:slug>', views.doctorList, name='doctorlist'),
    path('doctors/all', views.allDoctorList, name='doctor-all'),
    path('doctors/<int:pk>', views.doctor, name='doctor'),
    path('doctors/<int:pk>/book-appointment', views.bookAppointment, name='book-appointment'),

    path('prescriptions', views.prescription, name='prescription'),

    path('patient/', views.patient_profile, name='patient-profile'),
    path('patient/appointments', views.patient_appointments, name='patient-appointments'),
    path('patient/prescriptions/', views.patient_prescriptions, name='patient-prescriptions'),
    path('patient/prescriptions/<int:pk>/', views.patient_prescription, name='patient-prescription'),

    path('doctor/', views.doctor_dashboard, name='doctor-dashboard'),
    path('doctor/profile/', views.doctor_profile, name='doctor-profile'),
    path('doctor/appointments/', views.doctor_appointments, name='doctor-appointments'),
    
    path('doctor/patients/', views.doctor_patients, name='doctor-patients-list'),
    path('doctor/patients/<int:pk>', views.doctor_patient_detail, name='doctor-patient'),

    path('doctor/prescriptions/', views.doctor_prescriptions, name='doctor-prescriptions'),
    path('doctor/prescriptions/create/<int:pk>', views.create_prescription, name='create-prescription'),
    path('doctor/prescriptions/<int:pk>/', views.doctor_prescription, name='doctor-prescription'),



    path('test', views.test, name='test')
]