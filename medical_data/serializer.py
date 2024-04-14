from rest_framework import serializers

from . import models


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Medication
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Prescription
        fields = '__all__'


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Diagnosis
        fields = '__all__'


class MedicalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MedicalImage
        fields = '__all__'
