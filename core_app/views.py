from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from authentication.permissions import CustomPatientPermission, CustomDoctorPermission
from . import models, serializers


class PatientView(generics.ListCreateAPIView):
    queryset = models.Patient.objects.all()
    serializer_class = serializer.PatientSerializer
    permission_classes = [permissions.IsAuthenticated, CustomPatientPermission]
    # pagination_class = PageNumberPagination


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Patient.objects.all()
    serializer_class = serializer.PatientSerializer
    permission_classes = [permissions.IsAuthenticated, CustomPatientPermission]


class DoctorView(generics.ListCreateAPIView):
    queryset = models.Doctor.objects.all()
    serializer_class = serializer.DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDoctorPermission]
    # pagination_class = PageNumberPagination


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Doctor.objects.all()
    serializer_class = serializer.DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDoctorPermission]


class PersonalDoctorView(generics.GenericAPIView):
    queryset = models.Doctor.objects.all()
    serializer_class = serializer.DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDoctorPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.id)[0]

    def patch(self, request):
        print("PATCH", request.data)
        doctor = self.get_queryset()
        serializer = self.serializer_class(doctor, data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = doctor.user
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        if 'email' in request.data:
            user.email = request.data['email']
        user.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        doctor = self.get_queryset()
        serializer = self.serializer_class(doctor, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PersonalPatientView(generics.GenericAPIView):
    queryset = models.Patient.objects.all()
    serializer_class = serializer.PatientSerializer
    permission_classes = [permissions.IsAuthenticated, CustomPatientPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.id)[0]

    def patch(self, request):
        patient = self.get_queryset()
        serializer = self.serializer_class(patient, data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = patient.user
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        if 'email' in request.data:
            user.email = request.data['email']
        user.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        patient = self.get_queryset()
        serializer = self.serializer_class(patient, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
