from rest_framework import serializers
from . import models


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorAvailabilityModel
        fields = ['doctor', 'date', 'start_time', 'end_time']


class AppointmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppointmentModel
        fields = ['patient', 'slot', 'status']
