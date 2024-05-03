from django.contrib import admin
from . import models


class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'state_id', 'get_email', 'age', 'dob', 'sex', 'height', 'weight', 'alcoholic',
        'smoker', 'heart_disease', 'hypertension', 'diabetes')
    search_fields = ('first_name', 'last_name', 'state_id')
    list_filter = ('sex', 'alcoholic', 'smoker', 'heart_disease', 'hypertension', 'diabetes')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'get_email', 'specialization', 'phone', 'work_location')
    search_fields = ('first_name', 'last_name')
    list_filter = ('specialization',)

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'date', 'time', 'reason', 'notes')
    search_fields = ('patient', 'doctor')
    list_filter = ('date', 'time')


admin.site.register(models.Patient, PatientAdmin)
admin.site.register(models.Doctor, DoctorAdmin)
admin.site.register(models.Appointment, AppointmentAdmin)
