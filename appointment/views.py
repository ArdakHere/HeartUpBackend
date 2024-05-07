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


class CreateTimeSlotsView(generics.GenericAPIView):
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
        doctor = request.user
        date = request.data.get('date')
        start_time_str = request.data.get('start_time')
        end_time_str = request.data.get('end_time')
        duration_minutes = request.data.get('duration_minutes', 30)

        models.DoctorAvailabilityModel.create_time_slots(doctor, date, start_time_str, end_time_str, duration_minutes)

        return Response({'message': 'Time slots created successfully'}, status=status.HTTP_201_CREATED)


class BookAppointmentView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    """
        API endpoint to book an appointment
        request.data = {
            "slot_id": 1
        }
    """

    def post(self, request, *args, **kwargs):
        patient = request.user
        slot_id = request.data.get('slot_id')

        slot = models.DoctorAvailabilityModel.objects.get(id=slot_id)

        # Check if the slot is already booked
        if models.AppointmentModel.objects.filter(slot=slot).status == 'APPROVED':
            return Response({'message': 'Slot already booked'}, status=status.HTTP_400_BAD_REQUEST)

        # if the lost is pending
        if models.AppointmentModel.objects.filter(slot=slot).status == 'PENDING':
            return Response({'message': 'Slot already booked'}, status=status.HTTP_400_BAD_REQUEST)

        models.AppointmentModel.objects.create(patient=patient, slot=slot)

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
