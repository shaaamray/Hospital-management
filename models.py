from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    doc_field_choices = (
        ('Heart', 'Heart'),
        ('Lungs', 'Lungs'),
        ('Kidney', 'Kidney'),
        ('Liver', 'Liver'),
        ('Medicine', 'Medicine'),
        ('Neurology', 'Neurology'),
        ('Oncology', 'Oncology'),
        ('Orthopedics', 'Orthopedics'),
        ('Paediatrics', 'Paediatrics'),
        ('Psychiatry', 'Psychiatry'),
        ('Surgery', 'Surgery'),
        ('Urology', 'Urology'),
    )

    lable = models.CharField(max_length=10, blank=True, null=True)

    name = models.CharField(max_length=200, null=True, blank=True)
    age = models.IntegerField(default=0, null=True, blank=True)

    #For Patients
    phone = models.CharField(max_length=11, null=True, blank=True)
    address = models.TextField(max_length=200, null=True, blank=True)

    #For Doctors
    field = models.CharField(max_length=100, choices=doc_field_choices, null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)

class Appointment(models.Model):
    status_choices = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    )

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor')
    field = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(default=True, blank=True)
    reason = models.TextField(max_length=500, null=True, blank=True)
    confirmed = models.CharField(max_length=10, default='Pending', choices=status_choices)
    prescription = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.reason[:20]