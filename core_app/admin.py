from django.contrib import admin
from . import models


class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'state_id', 'email', 'age', 'dob', 'sex', 'height', 'weight', 'alcoholic',
        'smoker', 'heart_disease', 'hypertension', 'diabetes')
    search_fields = ('first_name', 'last_name', 'state_id')
    list_filter = ('sex', 'alcoholic', 'smoker', 'heart_disease', 'hypertension', 'diabetes')


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'specialization')
    search_fields = ('first_name', 'last_name')
    list_filter = ('specialization',)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'date', 'time', 'reason', 'notes')
    search_fields = ('patient', 'doctor')
    list_filter = ('date', 'time')


admin.site.register(models.Patient, PatientAdmin)
admin.site.register(models.Doctor, DoctorAdmin)
admin.site.register(models.Appointment, AppointmentAdmin)
