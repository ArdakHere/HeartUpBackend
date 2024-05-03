from rest_framework import generics, permissions

from . import models, serializer


class PatientView(generics.ListCreateAPIView):
    queryset = models.Patient.objects.all()
    serializer_class = serializer.PatientSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Patient.objects.all()
    serializer_class = serializer.PatientSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]


class DoctorView(generics.ListCreateAPIView):
    queryset = models.Doctor.objects.all()
    serializer_class = serializer.DoctorSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Doctor.objects.all()
    serializer_class = serializer.DoctorSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]


class AppointmentView(generics.ListCreateAPIView):
    queryset = models.Appointment.objects.all()
    serializer_class = serializer.AppointmentSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Appointment.objects.all()
    serializer_class = serializer.AppointmentSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]
