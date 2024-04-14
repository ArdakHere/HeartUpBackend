from django.contrib import admin
from . import models


class MedicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name', 'description')
    list_filter = ('name', 'description')


class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'appointment_id', 'medication_id', 'doctor_id', 'patient_id', 'date')
    search_fields = ('appointment_id', 'medication_id', 'doctor_id', 'patient_id', 'date')
    list_filter = ('date',)


class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('id', 'appointment_id', 'doctor_id', 'code', 'date', 'notes')
    search_fields = ('appointment_id', 'doctor_id', 'patient_id', 'code', 'date', 'notes')
    list_filter = ('date',)


class MedicalImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_type', 'image', 'appointment_id', 'patient_id', 'description')
    search_fields = ('image_type',)
    list_filter = ('image_type',)


admin.site.register(models.Medication, MedicationAdmin)
admin.site.register(models.Prescription, PrescriptionAdmin)
admin.site.register(models.Diagnosis, DiagnosisAdmin)
admin.site.register(models.MedicalImage, MedicalImageAdmin)
