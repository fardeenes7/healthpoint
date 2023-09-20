#create appointment booking form
# Path: core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'name', 'age', 'email', 'phone', 'address', 'date', 'time']


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PatientRegisterForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'phone', 'address']

class PatientProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'phone', 'address', 'image']

class PatientSettingsForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email']
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            pass
        return password
    

class DoctorProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'phone', 'address', 'image', 'bio']

class DoctorProfessionalUpdateForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['workplace','degree', 'bmdc']

class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedules
        fields = ['day', 'start_time', 'end_time']

class DoctorSettingsForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email']
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            pass
        return password


class PrescriptionUpdateForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['name', 'age', 'phone', 'email', 'address','cc', 'diagnosis', 'tx', 'advice', 'followup']