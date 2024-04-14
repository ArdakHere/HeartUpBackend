from rest_framework import generics

from . import models, serializer


class PatientView(generics.ListCreateAPIView):
    queryset = models.Patient.objects.all()
    serializer_class = serializer.PatientSerializer


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Patient.objects.all()
    serializer_class = serializer.PatientSerializer


class DoctorView(generics.ListCreateAPIView):
    queryset = models.Doctor.objects.all()
    serializer_class = serializer.DoctorSerializer


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Doctor.objects.all()
    serializer_class = serializer.DoctorSerializer


class AppointmentView(generics.ListCreateAPIView):
    queryset = models.Appointment.objects.all()
    serializer_class = serializer.AppointmentSerializer
