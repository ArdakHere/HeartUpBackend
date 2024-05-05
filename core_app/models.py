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

    state_id = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    dob = models.DateField()
    sex = models.CharField(max_length=10, choices=SEX_TYPE)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        self.user.role = 'PATIENT'
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pk} {self.user.first_name} {self.user.last_name} {self.state_id} {self.user.email}"


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

    phone = models.CharField(max_length=15)
    specialization = models.CharField(max_length=100, choices=SPECIALIZATION)
    aboutme = models.TextField(blank=True)
    work_location = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.user.role = 'DOCTOR'
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pk} {self.user.first_name} {self.user.last_name} {self.user.email} {self.specialization}"
