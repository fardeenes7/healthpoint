from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Speciality(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)
    icon = models.ImageField(upload_to='images/specialty/')
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = self.slug if self.slug else self.name.replace(' ', '-').replace('/','-').lower()
        super(Speciality, self).save(*args, **kwargs)
    

class Schedules(models.Model):
    DAYS = (
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday','Friday'),
    )
    
    day = models.CharField(max_length=100, choices=DAYS, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.day + ': ' + str(self.start_time) + ' to ' + str(self.end_time)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    workplace = models.CharField(max_length=100, default="N/A")
    degree = models.CharField(max_length=100, null=True, blank=True)
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True)
    bmdc = models.IntegerField()
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/doctors/', null=True, blank=True)
    schedules = models.ManyToManyField(Schedules)
    consultation = models.IntegerField()
    followup = models.IntegerField()
    percentage = models.IntegerField()
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/patients/', null=True, blank=True)

    def __str__(self):
        return self.name
    

class Appointment(models.Model):
    
    STATUS = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=100, choices=STATUS, null=True, default='Confirmed')
    note = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.patient.name + ' - ' + self.doctor.name + ' - ' + str(self.date) + ' - ' + str(self.time)
    

class Medication(models.Model):
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    note = models.CharField(max_length=100, null=True)
    prescription = models.ForeignKey('Prescription', related_name='medications', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    appointment = models.ForeignKey(Appointment, related_name='prescription', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    cc = models.TextField(null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)
    tx = models.TextField(null=True, blank=True)
    advice = models.TextField(null=True, blank=True)
    followup = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.patient.name + ' - ' + self.doctor.name + ' - ' + str(self.date)


class Revenue(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    amount = models.IntegerField(null=True, blank=True)
    doctor_amount = models.IntegerField(null=True, blank=True)
    clinic_amount = models.IntegerField(null=True, blank=True)
    isFollowup = models.BooleanField(default=False)

    def __str__(self):
        return self.doctor.name + ' - ' + str(self.date) + ' - ' + str(self.amount)
    
    def save(self, *args, **kwargs):
        if self.isFollowup:
            self.clinic_amount = self.amount*self.doctor.percentage if self.amount else self.doctor.followup*self.doctor.percentage/100
            self.doctor_amount = self.amount - self.clinic_amount if self.amount else self.doctor.followup - self.clinic_amount
        else:
            self.clinic_amount = self.amount*self.doctor.percentage if self.amount else self.doctor.consultation*self.doctor.percentage/100
            self.doctor_amount = self.amount - self.clinic_amount if self.amount else self.doctor.consultation - self.clinic_amount
        super(Revenue, self).save(*args, **kwargs)



def get_user_role(self):
    if Doctor.objects.filter(user=self).exists():
        return 'doctor'
    elif Patient.objects.filter(user=self).exists():
        return 'patient'
    elif self.is_superuser:
        return 'admin'
    

def get_profile_picture(self):
    if self.get_user_role() == 'doctor':
        return Doctor.objects.get(user=self).image
    elif self.get_user_role() == 'patient':
        return Patient.objects.get(user=self).image
    
def is_doctor(self):
    if Doctor.objects.filter(user=self).exists():
        return True
    else:
        return False
    
def is_patient(self):
    if Patient.objects.filter(user=self).exists():
        return True
    else:
        return False
    
User.add_to_class('get_user_role', get_user_role)
User.add_to_class('get_profile_picture', get_profile_picture)
User.add_to_class('is_doctor', is_doctor)
User.add_to_class('is_patient', is_patient)