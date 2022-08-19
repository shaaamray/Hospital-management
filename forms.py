from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Appointment

class PatientRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'age', 'phone', 'address', 'email', 'password1', 'password2']

class DoctorRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'field', 'password1', 'password2']

class EditAppointmentPatientForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'reason']

class PrescribePatientForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['prescription', 'confirmed']