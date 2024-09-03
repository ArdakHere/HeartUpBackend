from django.contrib import admin
from . import models


class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'state_id', 'get_full_name', 'get_email', 'age', 'dob', 'sex')
    search_fields = ('get_full_name', 'state_id')
    list_filter = ('sex', 'dob')

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'Email'

    def get_full_name(self, obj):
        return obj.user.get_full_name

    get_full_name.short_description = 'Name'


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_full_name', 'get_email', 'specialization', 'phone', 'work_location')
    search_fields = ('get_full_name', 'specialization', 'phone', 'work_location')
    list_filter = ('specialization',)

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'Email'

    def get_full_name(self, obj):
        return obj.user.get_full_name

    get_full_name.short_description = 'Name'


admin.site.register(models.Patient, PatientAdmin)
admin.site.register(models.Doctor, DoctorAdmin)
