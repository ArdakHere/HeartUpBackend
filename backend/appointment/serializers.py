from rest_framework import serializers
from . import models


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorAvailabilityModel
        fields = ['id', 'doctor', 'date', 'start_time', 'end_time']


class AppointmentModelSerializer(serializers.ModelSerializer):
    patient_first_name = serializers.CharField(source='patient.first_name', read_only=True)
    patient_last_name = serializers.CharField(source='patient.last_name', read_only=True)
    patient_email = serializers.CharField(source='patient.email', read_only=True)
    doctor_first_name = serializers.CharField(source='slot.doctor.first_name', read_only=True)
    doctor_last_name = serializers.CharField(source='slot.doctor.last_name', read_only=True)
    doctor_email = serializers.CharField(source='slot.doctor.email', read_only=True)
    date = serializers.DateField(source='slot.date', read_only=True)
    start_time = serializers.TimeField(source='slot.start_time', read_only=True)
    end_time = serializers.TimeField(source='slot.end_time', read_only=True)

    class Meta:
        model = models.AppointmentModel
        fields = ['id', 'patient', 'slot', 'status', 'patient_first_name', 'patient_last_name', 'patient_email',
                  'doctor_first_name', 'doctor_last_name', 'doctor_email', 'date', 'start_time', 'end_time']
