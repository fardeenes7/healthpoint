from datetime import datetime, timedelta
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import json
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
# Create your views here.


url = 'http://127.0.0.0:8000/' if settings.DEBUG == True else 'https://healthpoint.pythonanywhere.com/'
"""
Authentications
"""

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    data = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email.__contains__('@'):
            try:
                username = User.objects.get(email=email)
                user = authenticate(username=username.username, password=password)
            except:
                return render(request, 'landing/auth/login.html', {'status': 'error', 'message': 'Username or password is incorrect'})
        else:
            user = authenticate(username=email, password=password)

        if user is None:
            data['status'] = 'error'
            data['message'] = 'Username or password is incorrect'
        else:
            auth_login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            elif user.is_patient():
                return redirect('patient-profile')
            elif user.is_doctor():
                return redirect('doctor-dashboard')
            else:
                return redirect('/admin')
    return render(request, 'landing/auth/login.html', data)



def send_registration_email(patient):
    subject = 'Registration Successful'
    message = render_to_string('email/registration_email.html', {
        'reciever': patient.name, 'email': patient.user.email, 'title': 'Registration Successful', 'url': url
    })
    email_from = f'Healthpoint <{settings.EMAIL_HOST_USER}>'
    recipient_list = [patient.user.email, ]
    # send_mail( subject, message, email_from, recipient_list
    email = EmailMessage(
        subject,
        message,
        'Healthpoint Clinic<'+settings.EMAIL_HOST_USER+'>',
        recipient_list,
    )
    email.content_subtype = "html"
    email.send()


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            name = request.POST.get('name')
            age = request.POST.get('age')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            patient = Patient.objects.create(user=user, name=name, age=age, phone=phone, address=address)
            patient.save()
            auth_login(request, user)
            send_registration_email(patient)
            return redirect('patient-profile')
        else:
            messages.error(request, 'Registration Failed')
            error = form.errors
            return render(request, 'landing/auth/register.html', {'form': form, 'errors': error})
    return render(request, 'landing/auth/register.html')

def logout(request):
    auth_logout(request)
    return redirect('/login')


def about(request):
    return render(request, 'landing/about/about.html')

def privacy(request):
    return render(request, 'landing/about/privacy.html')

def terms(request):
    return render(request, 'landing/about/terms.html')

def disclaimer(request):
    return render(request, 'landing/about/disclaimer.html')



"""
Landing Pages
"""

@login_required(login_url="/login")
def prescription(request):
    prescription = Prescription.objects.get(pk=request.GET.get('id'))
    if request.user.is_doctor():
        return redirect('doctor-prescription', pk=prescription.id)
    elif request.user.is_patient():
        if prescription.patient.user == request.user:
            return redirect('patient-prescription', pk=prescription.id)
        else:
            return redirect('patient-prescriptions')


def index(request):
    return render(request, 'landing/index.html')


def specialityList(request):
    data = {}
    data['specialities'] = Speciality.objects.all()
    return render(request, 'landing/doctors/specialities.html', data)

def doctorList(request, slug):
    if slug=="":
        return redirect('specialities')
    data = {}
    data['doctors'] = Doctor.objects.filter(speciality__slug=slug)
    return render(request, 'landing/doctors/doctor-list.html', data)


def allDoctorList(request):
    data = {}
    data['doctors'] = Doctor.objects.all()
    data['all_doctor'] = True
    return render(request, 'landing/doctors/doctor-list.html', data)


def doctor(request, pk):
    data = {}
    data['doctor'] = Doctor.objects.get(pk=pk)
    data['patient_count'] = Prescription.objects.filter(doctor=data['doctor']).count()
    data['schedules'] = data['doctor'].schedules.all()
    return render(request, 'landing/doctors/doctor-profile.html', data)

def send_booking_confirmation_email(appointment):
    subject = 'Appointment Confirmation'
    message = render_to_string('email/booking_confirmation.html', {
        'appointment': appointment, 'reciever': appointment.name, 'email': appointment.email, 'title': 'Your appointment has been confirmed.', 'url': url
    })
    email_from = f'Healthpoint <{settings.EMAIL_HOST_USER}>'
    recipient_list = [appointment.email, ]
    # send_mail( subject, message, email_from, recipient_list
    email = EmailMessage(
        subject,
        message,
        'Healthpoint Clinic<'+settings.EMAIL_HOST_USER+'>',
        recipient_list,
    )
    email.content_subtype = "html"
    email.send()


def test(request):
    appointment = Appointment.objects.all().last()
    # send_booking_confirmation_email(appointment)
    patient = Patient.objects.all().last()
    return render(request, 'email/registration_email.html', { 'reciever': patient.name, 'email': patient.user.email, 'title': 'Registration Successful'})


@login_required(login_url="/login")
def bookAppointment(request, pk):
    if not request.user.is_patient():
        return redirect('/')
    # if not request.user.is_authenticated:
    #     return redirect(f'{settings.LOGIN_URL}?next={request.path}')
    data = {}
    data['doctor'] = Doctor.objects.get(pk=pk)
    data['patient'] = Patient.objects.get(user=request.user)
    data['is_first_visit'] = True if Prescription.objects.filter(patient=data['patient'], doctor=data['doctor']).count() == 0 else False
    data['dates'] = {}
    for i in range(0, 30):
        day = (datetime.now() + timedelta(days=i)).strftime('%A')
        days = [schedule.day for schedule in data['doctor'].schedules.all()]
        if day in days:
            date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
            data['dates'][date] = {}
            #convert date to j M, Y format
            data['dates'][date]['date'] = (datetime.now() + timedelta(days=i)).strftime('%d %B, %Y')
            data['dates'][date]['day'] = (datetime.now() + timedelta(days=i)).strftime('%A')
            data['dates'][date]['slots'] = {}
            # calculate slots in 15 minutes interva fron start_time and end_time
            # start_time = str(data['doctor'].schedules.get(day=day).start_time)
            # end_time = str(data['doctor'].schedules.get(day=day).end_time)
            start_time = datetime.strptime(str(data['doctor'].schedules.get(day=day).start_time), '%H:%M:%S')
            end_time = datetime.strptime(str(data['doctor'].schedules.get(day=day).end_time), '%H:%M:%S')
            # print(start_time, end_time)
            while start_time < end_time:
                time = start_time.strftime('%I:%M %p')
                #convert this to django timefield
                converted_time = datetime.strptime(time, '%I:%M %p').time()
                if Appointment.objects.filter(doctor=data['doctor'], date=date, time=converted_time).count() > 0:
                    data['dates'][date]['slots'][start_time.strftime('%I:%M %p')] = 'booked'
                    
                else:
                    data['dates'][date]['slots'][start_time.strftime('%I:%M %p')] = 'open'
                    # data['dates'][date]['slots'][start_time.strftime('%I:%M %p')] = [start_time, 'open']                    
                start_time = start_time + timedelta(minutes=15)
            data['dates'][date]['slots'] = json.dumps(data['dates'][date]['slots'])
    
    
    if request.method == 'POST':
        # modify time before saving form
        request.POST._mutable = True
        request.POST['time'] = datetime.strptime(request.POST['time'], '%I:%M %p').time()
        request.POST['date'] = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
        request.POST['doctor'] = Doctor.objects.get(pk=pk)
        request.POST['patient'] = Patient.objects.get(user=request.user)
        print(request.POST)
        form = AppointmentForm(request.POST)
        if form.is_valid():
            print('valid')
            form.save()
            messages.success(request, 'Your appointment has been confirmed.')
            send_booking_confirmation_email(form.instance)
            return redirect('patient-appointments')

        else:
            messages.error(request, 'Something went wrong. Please try again.')
            return render(request, 'landing/doctors/book-appointment.html', data)


    return render(request, 'landing/doctors/book-appointment.html', data)





"""
Patient Dashboard
"""



@login_required(login_url="/login")
def patient_profile(request):
    if not request.user.is_patient():
        return redirect('/')
    data ={}
    if request.method == 'POST':
        if request.POST['action'] == 'personal':
            form = PatientProfileUpdateForm(request.POST, request.FILES, instance=Patient.objects.get(user=request.user))
        elif request.POST['action'] == 'settings':
            form = PatientSettingsForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('patient-profile')
        else:
            data[request.POST['action']+'error'] = form.errors
            messages.error(request, 'Something went wrong. Please try again.')
    data['patient'] = Patient.objects.get(user=request.user)
    return render(request, 'patient/profile.html', data)


@login_required(login_url="/login")
def patient_appointments(request):
    if not request.user.is_patient():
        return redirect('/')
    data ={}
    data['patient'] = Patient.objects.get(user=request.user)
    if request.GET.get('status'):
        data['appointments'] = Appointment.objects.filter(patient=data['patient'], status=request.GET.get('status')).order_by('-id')
    else:
        data['appointments'] = Appointment.objects.filter(patient=data['patient']).order_by('-id')
    return render(request, 'patient/appointments.html', data)


@login_required(login_url="/login")
def patient_prescriptions(request):
    if not request.user.is_patient():
        return redirect('/')
    data ={}
    data['patient'] = Patient.objects.get(user=request.user)
    data['prescriptions'] = Prescription.objects.filter(patient=data['patient']).order_by('-id')
    data['url'] = url
    return render(request, 'patient/prescriptions.html', data)


@login_required(login_url="/login")
def patient_prescription(request, pk):
    if not request.user.is_patient():
        return redirect('/')
    data ={}
    data['patient'] = Patient.objects.get(user=request.user)
    try:
        data['prescription'] = Prescription.objects.get(pk=pk, patient=data['patient'])
    except:
        return redirect('patient-prescriptions')
    data['url'] = url
    return render(request, 'patient/prescription.html', data)



"""
Doctor Dashboard
"""
@login_required(login_url="/login")
def doctor_dashboard(request):
    if not request.user.is_doctor():
        return redirect('/')
    data ={}
    data['doctor'] = Doctor.objects.get(user=request.user)
    data['appointments'] = Appointment.objects.filter(doctor=data['doctor'], date=datetime.now().date())
    stats ={}
    stats['appointments_today'] = data['appointments'].count()
    stats['total_patients'] = Appointment.objects.filter(doctor=data['doctor']).values('patient').distinct().count()
    stats['total_consultations'] = Prescription.objects.filter(doctor=data['doctor']).count()
    data['stats'] = stats
    return render(request, 'doctor/dashboard.html', data)


@login_required(login_url="/login")
def doctor_profile(request):
    if not request.user.is_doctor():
        return redirect('/')
    data ={}
    if request.method == 'POST':
        if request.POST['action'] == 'personal':
            form = DoctorProfileUpdateForm(request.POST, request.FILES, instance=Doctor.objects.get(user=request.user))
        elif request.POST['action'] == 'professional':
            form = DoctorProfessionalUpdateForm(request.POST, instance=Doctor.objects.get(user=request.user))
        elif request.POST['action'] == 'settings':
            form = DoctorSettingsForm(request.POST, instance=request.user)
        

        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('doctor-profile')
        else:
            data[request.POST['action']+'error'] = form.errors
            print(form.errors)
    data['doctor'] = Doctor.objects.get(user=request.user)
    return render(request, 'doctor/profile.html', data)


@login_required(login_url="/login")
def doctor_appointments(request):
    if not request.user.is_doctor():
        return redirect('/')
    data ={}
    data['doctor'] = Doctor.objects.get(user=request.user)
    if request.GET.get('status'):
        data['appointments'] = Appointment.objects.filter(doctor=data['doctor'], status=request.GET.get('status')).order_by('-id')
    else:
        data['appointments'] = Appointment.objects.filter(doctor=data['doctor']).order_by('-id')
    return render(request, 'doctor/appointments.html', data)


@login_required(login_url="/login")
def doctor_patients(request):
    if not request.user.is_doctor():
        return redirect('/')
    data ={}
    data['doctor'] = Doctor.objects.get(user=request.user)
    data['patients'] = Patient.objects.filter(appointment__doctor=data['doctor']).distinct()
    return render(request, 'doctor/patients.html', data)


@login_required(login_url="/login")
def doctor_patient_detail(request, pk):
    if not request.user.is_doctor():
        return redirect('/')
    data ={}
    data['doctor'] = Doctor.objects.get(user=request.user)
    data['patient'] = Patient.objects.get(pk=pk)
    data['last_visit'] = Prescription.objects.filter(doctor=data['doctor'], patient=data['patient']).order_by('-id').first().date if Prescription.objects.filter(doctor=data['doctor'], patient=data['patient']).order_by('-id').first() else None
    data['appointments'] = Appointment.objects.filter(doctor=data['doctor'], patient=data['patient']).order_by('-id')
    if request.GET.get('doctor'):
        data['prescriptions'] = Prescription.objects.filter(doctor=data['doctor'], patient=data['patient']).order_by('-id')
    else:
        data['prescriptions'] = Prescription.objects.filter(patient=data['patient']).order_by('-id')
    data['url'] = url
    return render(request, 'doctor/patient-detail.html', data)


@login_required(login_url="/login")
def create_prescription(request, pk):
    if not request.user.is_doctor():
        return redirect('/')
    doctor = Doctor.objects.get(user=request.user)
    patient = Patient.objects.get(pk=pk)
    name = request.POST.get('name')
    age = request.POST.get('age') if request.POST.get('age')!='None' else None
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    appointment = Appointment.objects.get(pk=request.POST.get('appointment'))
    appointment.status = 'Completed'
    appointment.save()
    prescription = Prescription.objects.create(doctor=doctor, patient=patient, name=name, age=age, email=email, phone=phone, address=address, appointment=appointment)
    messages.success(request, 'Prescription created successfully.')
    return redirect('doctor-prescription', prescription.pk)

@login_required(login_url="/login")
def doctor_prescriptions(request):
    if not request.user.is_doctor():
        return redirect('/')
    data ={}
    data['doctor'] = Doctor.objects.get(user=request.user)
    data['prescriptions'] = Prescription.objects.filter(doctor=data['doctor'])
    data['url'] = url
    return render(request, 'doctor/prescription.html', data)



def send_prescription(prescription):
    subject = 'Your Prescription is Ready'
    message = render_to_string('email/send_prescription.html', {
        'prescription': prescription, 'reciever': prescription.name, 'email': prescription.email, 'title': 'View your prescription online', 'url': url
    })
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [prescription.email ]
    # send_mail( subject, message, email_from, recipient_list
    email = EmailMessage(
        subject,
        message,
        'Healthpoint Clinic<'+settings.EMAIL_HOST_USER+'>',
        recipient_list,
    )
    email.content_subtype = "html"
    email.send()


@login_required(login_url="/login")
def doctor_prescription(request, pk):
    if not request.user.is_doctor():
        return redirect('/')
    data ={}
    data['doctor'] = Doctor.objects.get(user=request.user)
    data['prescription'] = Prescription.objects.get(pk=pk)
    data['medications'] = Medication.objects.filter(prescription=data['prescription'])
    data['form'] = PrescriptionUpdateForm(instance=data['prescription'])
    if request.method=="POST":
        if request.POST.get('action') == 'send_email':
            send_prescription(data['prescription'])
            messages.success(request, 'Email sent successfully.')
        elif request.POST.get('action') == 'addmedicine':
            Medication.objects.create(prescription=data['prescription'], name=request.POST.get('medicinename'), dosage=request.POST.get('dosage'), duration=request.POST.get('duration'), note=request.POST.get('note'))
            messages.success(request, 'Medicine added successfully.')
        elif request.POST.get('action') == 'update':
            form = PrescriptionUpdateForm(request.POST, instance=data['prescription'])
            if form.is_valid():
                form.save()
                messages.success(request, 'Prescription updated successfully.')
        return redirect('doctor-prescription', pk)
    data['url'] = url
    return render(request, 'doctor/prescription.html', data)




