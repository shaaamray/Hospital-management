from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .decorators import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .decorators import *

# Create your views here.
def homePage(request):
    return render(request, 'hmapp/index.html')


def logoutUser(request):
    logout(request)
    return redirect('home')

def patientRegistration(request):
    form = PatientRegistrationForm()

    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save()
            group = Group.objects.get(name='patient')
            patient.groups.add(group)
            return redirect('login')

    context = {
        'form': form,
    }
    return render(request, 'hmapp/patient_registration.html', context)

def doctorRegistration(request):
    form = DoctorRegistrationForm()

    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            group = Group.objects.get(name='admin')
            doctor.groups.add(group)
            return redirect('login')

    context = {
        'form': form
    }

    return render(request, 'hmapp/doctor_registration.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return redirect('login')
    return render(request, 'hmapp/login.html')

@login_required(login_url='login')
#@allowed_users(allowed_roles=['patient'])
def dasboardPage(request):
    if 'Q' in request.GET:
        q = request.GET['Q']
        docs = User.objects.filter(field__istartswith=q)
    else:
        docs = User.objects.filter(name__istartswith='Dr.')

    context = {
        'docs': docs
    }
    return render(request, 'hmapp/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def bookAppointment(request, pk):
    doc = User.objects.get(id=pk)

    if request.method == 'POST':
        patient = request.user
        doc = User.objects.get(id=pk)
        field = request.POST.get('doc_specialization')
        date = request.POST.get('expected_appointment_date')
        reason = request.POST.get('history')

        appointment = Appointment(patient=patient, doctor=doc, field=field, date=date, reason=reason)
        appointment.save()

        return redirect('dashboard')

    context = {
        'doc': doc
    }
    return render(request, 'hmapp/book_appointment.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def patientAppointments(request):
    appointments = Appointment.objects.filter(patient=request.user)
    context = {
        'appointments': appointments
    }
    return render(request, 'hmapp/appointment_history.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def editAppointmentPatient(request, pk):
    data = Appointment.objects.get(id=pk)
    form = EditAppointmentPatientForm(instance=data)

    if request.method == 'POST':
        form = EditAppointmentPatientForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('patient-appointments')

    context = {
        'form': form
    }
    return render(request, 'hmapp/edit_appointment.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def deleteAppointmentPatient(request, pk):
    data = Appointment.objects.get(id=pk)

    if request.method == 'POST':
        data.delete()
        return redirect('patient-appointments')

    context = {
        'data': data
    }
    return render(request, 'hmapp/delete_appointment.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def doctorDashboard(request):

    appointments = Appointment.objects.filter(doctor=request.user)

    context = {
        'data': appointments
    }

    return render(request, 'hmapp/doctor_dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def doctorPatientView(request, pk):

    data = Appointment.objects.get(id=pk)

    context = {
        'data': data
    }

    return render(request, 'hmapp/doctor_patient_view.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def prescribePatient(request, pk):

    data = Appointment.objects.get(id=pk)
    form = PrescribePatientForm(instance=data)

    if request.method == 'POST':
        form = PrescribePatientForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('doctor-dashboard')

    context = {
        'form': form
    }

    return render(request, 'hmapp/prescribe_patient.html', context)