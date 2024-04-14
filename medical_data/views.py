from rest_framework import generics

from . import models, serializer


class MedicationView(generics.ListCreateAPIView):
    queryset = models.Medication.objects.all()
    serializer_class = serializer.MedicationSerializer


class MedicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Medication.objects.all()
    serializer_class = serializer.MedicationSerializer


class PrescriptionView(generics.ListCreateAPIView):
    queryset = models.Prescription.objects.all()
    serializer_class = serializer.PrescriptionSerializer


class PrescriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Prescription.objects.all()
    serializer_class = serializer.PrescriptionSerializer


class DiagnosisView(generics.ListCreateAPIView):
    queryset = models.Diagnosis.objects.all()
    serializer_class = serializer.DiagnosisSerializer


class DiagnosisDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Diagnosis.objects.all()
    serializer_class = serializer.DiagnosisSerializer


class MedicalImageView(generics.ListCreateAPIView):
    queryset = models.MedicalImage.objects.all()
    serializer_class = serializer.MedicalImageSerializer


class MedicalImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MedicalImage.objects.all()
    serializer_class = serializer.MedicalImageSerializer
