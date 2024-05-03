from rest_framework import serializers

from . import models


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Patient

        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = models.User.objects.create_user(**user_data)
        patient = models.Patient.objects.create(user=user, **validated_data)
        return patient


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Doctor
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = models.User.objects.create_user(**user_data)
        doctor = models.Doctor.objects.create(user=user, **validated_data)
        return doctor


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Appointment
        fields = '__all__'
