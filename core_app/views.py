from rest_framework import generics, permissions

from authentication.permissions import IsDoctorOrIsPatient, CanWriteIfAdmin, CanWriteIfOwnerOrAdmin
from . import models, serializer


class PatientView(generics.ListCreateAPIView):
    queryset = models.Patient.objects.all()
    serializer_class = serializer.PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrIsPatient, CanWriteIfAdmin]


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Patient.objects.all()
    serializer_class = serializer.PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrIsPatient, CanWriteIfAdmin]


class DoctorView(generics.ListCreateAPIView):
    queryset = models.Doctor.objects.all()
    serializer_class = serializer.DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrIsPatient, CanWriteIfAdmin]


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Doctor.objects.all()
    serializer_class = serializer.DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrIsPatient, CanWriteIfOwnerOrAdmin]
