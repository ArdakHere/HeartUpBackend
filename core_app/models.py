from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.db import models

from authentication.models import User


class Patient(models.Model):
    SEX_TYPE = (
        ('male', 'male'),
        ('female', 'female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')

    photo = models.ImageField(upload_to='patient_photos', blank=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    state_id = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    dob = models.DateField()
    sex = models.CharField(max_length=10, choices=SEX_TYPE)

    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    alcoholic = models.BooleanField(default=False)
    smoker = models.BooleanField(default=False)
    heart_disease = models.BooleanField(default=False)
    hypertension = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk} {self.first_name} {self.last_name} {self.state_id} {self.user.email}"


class Doctor(models.Model):
    SPECIALIZATION = (
        ('cardiologist', 'cardiologist'),
        ('dermatologist', 'dermatologist'),
        ('endocrinologist', 'endocrinologist'),
        ('gastroenterologist', 'gastroenterologist'),
        ('nephrologist', 'nephrologist'),
        ('neurologist', 'neurologist'),
        ('oncologist', 'oncologist'),
        ('ophthalmologist', 'ophthalmologist'),
        ('pediatrician', 'pediatrician'),
        ('psychiatrist', 'psychiatrist'),
        ('pulmonologist', 'pulmonologist'),
        ('radiologist', 'radiologist'),
        ('rheumatologist', 'rheumatologist'),
        ('urologist', 'urologist')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')

    photo = models.ImageField(upload_to='doctor_photos', blank=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    specialization = models.CharField(max_length=100, choices=SPECIALIZATION)
    aboutme = models.TextField(blank=True)
    work_location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.pk} {self.first_name} {self.last_name} {self.user.email} {self.specialization}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.pk} {self.patient} {self.doctor} {self.date} {self.time}"
