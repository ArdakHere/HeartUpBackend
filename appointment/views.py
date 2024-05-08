from datetime import datetime

from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from notification.models import NotificationModel
from . import models
from . import serializers
from .utils import send_normal_email


class DoctorAvailabilityListCreateView(generics.ListCreateAPIView):
    queryset = models.DoctorAvailabilityModel.objects.all()
    serializer_class = serializers.DoctorAvailabilitySerializer
    permission_classes = [permissions.AllowAny]


class DoctorAvailabilityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.DoctorAvailabilityModel.objects.all()
    serializer_class = serializers.DoctorAvailabilitySerializer
    permission_classes = [permissions.AllowAny]


class AppointmentModelListCreateView(generics.ListCreateAPIView):
    queryset = models.AppointmentModel.objects.all()
    serializer_class = serializers.AppointmentModelSerializer
    permission_classes = [permissions.AllowAny]


class AppointmentModelRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.AppointmentModel.objects.all()
    serializer_class = serializers.AppointmentModelSerializer
    permission_classes = [permissions.AllowAny]


class DoctorTimeSlotsByDateView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    """
        API endpoint to get time slots for a doctor by date
        request.GET = {
            "date": "YYYY-MM-DD"
        }
    """

    def get(self, request, *args, **kwargs):
        doctor = request.user
        date = request.GET.get('date')
        if date:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            time_slots = models.DoctorAvailabilityModel.objects.filter(doctor=doctor, date=date_obj).order_by(
                'start_time')
        else:
            return Response({'message': 'Date is required'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.DoctorAvailabilitySerializer(time_slots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorTimeSlotsView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    """
        API endpoint to create time slots for a doctor
        request.data = {
            "date": "YYYY-MM-DD",
            "start_time": "HH:MM",
            "end_time": "HH:MM",
            "duration_minutes": 30
        }
    """

    def post(self, request, *args, **kwargs):
        if request.user.role != 'DOCTOR':
            return Response({'message': 'Only doctors can create time slots'}, status=status.HTTP_400_BAD_REQUEST)

        doctor = request.user
        date = request.data.get('date')
        start_time_str = request.data.get('start_time')
        end_time_str = request.data.get('end_time')
        duration_minutes = request.data.get('duration_minutes', 30)

        models.DoctorAvailabilityModel.create_time_slots(doctor, date, start_time_str, end_time_str, duration_minutes)
        return Response({'message': 'Time slots created successfully'}, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        doctor = request.user
        today = timezone.now().date()
        time_slots = models.DoctorAvailabilityModel.objects.filter(doctor=doctor, date__gte=today).order_by('date',
                                                                                                            'start_time')
        serializer = serializers.DoctorAvailabilitySerializer(time_slots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookAppointmentView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    """
        API endpoint to book an appointment
        request.data = {
            "slot_id": 1
        }
    """

    def post(self, request, *args, **kwargs):
        if request.user.role != 'PATIENT':
            return Response({'message': 'Only patients can book appointments'}, status=status.HTTP_400_BAD_REQUEST)

        patient = request.user
        slot_id = request.data.get('slot_id')

        slot = models.DoctorAvailabilityModel.objects.get(id=slot_id)

        # Check if the slot is already booked
        if models.AppointmentModel.objects.filter(slot=slot, status='APPROVED').exists():
            return Response({'message': 'Slot already booked'}, status=status.HTTP_400_BAD_REQUEST)

        # if the lost is pending
        if models.AppointmentModel.objects.filter(slot=slot, status='PENDING').exists():
            return Response({'message': 'Slot already booked'}, status=status.HTTP_400_BAD_REQUEST)

        models.AppointmentModel.objects.create(patient=patient, slot=slot)

        # Create a new notification for the doctor
        NotificationModel.objects.create(
            user=slot.doctor,
            subject='New Appointment Request',
            message=f'You have a new appointment request from {patient.first_name} {patient.last_name}.'
        )

        return Response({'message': 'Appointment booked successfully'}, status=status.HTTP_201_CREATED)


class ApproveAppointmentView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    """
        API endpoint to approve an appointment
        request.data = {
            "appointment_id": 1
        }
    """

    def post(self, request, *args, **kwargs):
        if request.user.role != 'DOCTOR':
            return Response({'message': 'Only doctor can approve appointment'}, status=status.HTTP_400_BAD_REQUEST)
        appointment_id = request.data.get('appointment_id')

        appointment = models.AppointmentModel.objects.get(id=appointment_id)
        appointment.status = 'APPROVED'
        appointment.save()

        # Reject all other appointments for the same slot
        models.AppointmentModel.objects.filter(slot=appointment.slot).exclude(id=appointment_id).update(
            status='REJECTED')

        # Send email to patient
        email_data = {
            'email_subject': 'Appointment Approved',
            'email_body': f'Your appointment has been approved. '
                          f'Doctor: {appointment.slot.doctor.email}, '
                          f'Date: {appointment.slot.date}, '
                          f'Start Time: {appointment.slot.start_time}, '
                          f'End Time: {appointment.slot.end_time}',
            'to_email': [appointment.patient.email]
        }
        send_normal_email(email_data)

        # Send email for other appointments that were rejected
        rejected_appointments = models.AppointmentModel.objects.filter(slot=appointment.slot).exclude(id=appointment_id)
        email_list = []
        for rejected_appointment in rejected_appointments:
            email_list.append(rejected_appointment.patient.email)

            # Create new notification for rejected patient's appointments
            NotificationModel.objects.create(
                user=rejected_appointment.patient,
                subject='Appointment Rejected',
                message=f'Your appointment has been rejected. '
                        f'Doctor: {appointment.slot.doctor.email}, '
                        f'Date: {appointment.slot.date}, '
                        f'Start Time: {appointment.slot.start_time}, '
                        f'End Time: {appointment.slot.end_time}'
            )

        email_data = {
            'email_subject': 'Appointment Rejected',
            'email_body': f'Your appointment has been rejected. '
                          f'Doctor: {appointment.slot.doctor.email}, '
                          f'Date: {appointment.slot.date}, '
                          f'Start Time: {appointment.slot.start_time}, '
                          f'End Time: {appointment.slot.end_time}',
            'to_email': email_list
        }
        send_normal_email(email_data)

        # Create a new notification
        NotificationModel.objects.create(
            user=appointment.patient,
            subject='Appointment Approved',
            message=f'Your appointment has been approved. '
                    f'Doctor: {appointment.slot.doctor.email}, '
                    f'Date: {appointment.slot.date}, '
                    f'Start Time: {appointment.slot.start_time}, '
                    f'End Time: {appointment.slot.end_time}'
        )

        return Response({'message': 'Appointment approved successfully'}, status=status.HTTP_200_OK)


class RejectAppointmentView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    """
        API endpoint to reject an appointment
        request.data = {
            "appointment_id": 1
        }
    """

    def post(self, request, *args, **kwargs):
        if request.user.role != 'DOCTOR':
            return Response({'message': 'Only doctor can reject appointment'}, status=status.HTTP_400_BAD_REQUEST)

        appointment_id = request.data.get('appointment_id')

        appointment = models.AppointmentModel.objects.get(id=appointment_id)
        appointment.status = 'REJECTED'
        appointment.save()

        # Send email to patient
        email_data = {
            'email_subject': 'Appointment Rejected',
            'email_body': f'Your appointment has been rejected. '
                          f'Doctor: {appointment.slot.doctor.email}, '
                          f'Date: {appointment.slot.date}, '
                          f'Start Time: {appointment.slot.start_time}, '
                          f'End Time: {appointment.slot.end_time}',
            'to_email': [appointment.patient.email]
        }
        send_normal_email(email_data)

        # Create a new notification
        NotificationModel.objects.create(
            user=appointment.patient,
            subject='Appointment Rejected',
            message=f'Your appointment has been rejected. '
                    f'Doctor: {appointment.slot.doctor.email}, '
                    f'Date: {appointment.slot.date}, '
                    f'Start Time: {appointment.slot.start_time}, '
                    f'End Time: {appointment.slot.end_time}'
        )

        return Response({'message': 'Appointment rejected successfully'}, status=status.HTTP_200_OK)


class ApprovedAppointmentsListView(generics.ListAPIView):
    serializer_class = serializers.AppointmentModelSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return models.AppointmentModel.objects.filter(status='APPROVED')


class PendingAppointmentsListView(generics.ListAPIView):
    serializer_class = serializers.AppointmentModelSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return models.AppointmentModel.objects.filter(status='PENDING')


class RejectedAppointmentsListView(generics.ListAPIView):
    serializer_class = serializers.AppointmentModelSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return models.AppointmentModel.objects.filter(status='REJECTED')


class MyApprovedAppointmentsListView(generics.ListAPIView):
    serializer_class = serializers.AppointmentModelSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return models.AppointmentModel.objects.filter(status='APPROVED', patient=self.request.user)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        patient = request.user
        date = datetime.today().strftime('%Y-%m-%d')
        if date:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            time_slots = (
                models.AppointmentModel.objects.filter(patient=patient, slot__date__gte=date_obj, status='APPROVED')
                .order_by('slot__date', 'slot__start_time'))
            serializer = self.get_serializer(time_slots, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyPendingAppointmentsListView(generics.ListAPIView):
    serializer_class = serializers.AppointmentModelSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return models.AppointmentModel.objects.filter(status='PENDING', patient=self.request.user)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        patient = request.user
        date = datetime.today().strftime('%Y-%m-%d')
        if date:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            time_slots = (
                models.AppointmentModel.objects.filter(patient=patient, slot__date__gte=date_obj, status='PENDING')
                .order_by('slot__date', 'slot__start_time'))
            serializer = self.get_serializer(time_slots, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyRejectedAppointmentsListView(generics.ListAPIView):
    serializer_class = serializers.AppointmentModelSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return models.AppointmentModel.objects.filter(status='REJECTED', patient=self.request.user)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        patient = request.user
        date = datetime.today().strftime('%Y-%m-%d')
        if date:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            time_slots = (
                models.AppointmentModel.objects.filter(patient=patient, slot__date__gte=date_obj, status='REJECTED')
                .order_by('slot__date', 'slot__start_time'))
            serializer = self.get_serializer(time_slots, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyApprovedAppointmentsListDoctorView(generics.ListAPIView):
    serializer_class = serializers.AppointmentModelSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return models.AppointmentModel.objects.filter(status='APPROVED', slot__doctor=self.request.user)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        doctor = request.user
        date = datetime.today().strftime('%Y-%m-%d')
        if date:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            time_slots = (
                models.AppointmentModel.objects.filter(slot__doctor=doctor, slot__date__gte=date_obj, status='APPROVED')
                .order_by('slot__date', 'slot__start_time'))
            serializer = self.get_serializer(time_slots, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApprovedAppointmentsByDoctorView(generics.ListAPIView):
    serializer_class = serializers.AppointmentModelSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        date = datetime.today().strftime('%Y-%m-%d')
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        return models.AppointmentModel.objects.filter(slot__doctor_id=doctor_id, slot__date__gte=date_obj,
                                                      status='APPROVED').order_by('slot__date', 'slot__start_time')


class MyPendingAppointmentsListDoctorView(generics.ListAPIView):
    serializer_class = serializers.AppointmentModelSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return models.AppointmentModel.objects.filter(status='PENDING', slot__doctor=self.request.user)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        doctor = request.user
        date = datetime.today().strftime('%Y-%m-%d')
        if date:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            time_slots = (
                models.AppointmentModel.objects.filter(slot__doctor=doctor, slot__date__gte=date_obj, status='PENDING')
                .order_by('slot__start_time'))
            serializer = self.get_serializer(time_slots, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyRejectedAppointmentsListDoctorView(generics.ListAPIView):
    serializer_class = serializers.AppointmentModelSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return models.AppointmentModel.objects.filter(status='REJECTED', slot__doctor=self.request.user)


class SlotsByDoctorIdView(generics.ListAPIView):
    serializer_class = serializers.DoctorAvailabilitySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        return models.DoctorAvailabilityModel.objects.filter(doctor_id=doctor_id,
                                                             date__gte=timezone.now().date()).order_by('date',
                                                                                                       'start_time')


class SlotsByDoctorIdAndDateView(generics.ListAPIView):
    serializer_class = serializers.DoctorAvailabilitySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        date = self.kwargs.get('date')
        return models.DoctorAvailabilityModel.objects.filter(doctor_id=doctor_id, date=date).order_by('start_time')
