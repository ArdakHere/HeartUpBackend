from django.contrib import admin

from . import models


class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'get_date', 'get_start_time', 'get_end_time', 'status', 'get_doctor_email', 'get_patient_email')
    list_filter = (
    'status', 'slot__date', 'slot__start_time', 'slot__end_time', 'slot__doctor__email', 'patient__email')
    search_fields = ('get_date', 'get_start_time', 'get_end_time', 'status', 'get_doctor_email', 'get_patient_email')
    list_per_page = 25

    def get_doctor_email(self, obj):
        return obj.slot.doctor.email

    get_doctor_email.short_description = 'Doctor Email'

    def get_patient_email(self, obj):
        return obj.patient.email

    get_patient_email.short_description = 'Patient Email'

    def get_date(self, obj):
        return obj.slot.date

    get_date.short_description = 'Date'

    def get_start_time(self, obj):
        return obj.slot.start_time

    get_start_time.short_description = 'Start Time'

    def get_end_time(self, obj):
        return obj.slot.end_time

    get_end_time.short_description = 'End Time'


admin.site.register(models.AppointmentModel, AppointmentAdmin)
admin.site.register(models.DoctorAvailabilityModel)
