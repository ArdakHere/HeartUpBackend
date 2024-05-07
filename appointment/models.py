from datetime import datetime, timedelta

from django.db import models


class DoctorAvailabilityModel(models.Model):
    doctor = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='doctor_slot')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Doctor: {self.doctor}, Date: {self.date}, Start Time: {self.start_time}, End Time: {self.end_time}"

    @classmethod
    def create_time_slots(cls, doctor, date, start_time_str, end_time_str, duration_minutes=30):
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()
        duration = timedelta(minutes=duration_minutes)

        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        while start_time < end_time:
            slot_end_time = (datetime.combine(date_obj.min, start_time) + duration).time()

            if slot_end_time > end_time:
                break

            cls.objects.create(doctor=doctor, date=date, start_time=start_time, end_time=slot_end_time)
            start_time = slot_end_time


class AppointmentModel(models.Model):
    STATUS = (
        ('PENDING', 'PENDING'),
        ('APPROVED', 'APPROVED'),
        ('REJECTED', 'REJECTED')
    )

    patient = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='patient_appointment')
    slot = models.ForeignKey(DoctorAvailabilityModel, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(choices=STATUS, default='PENDING')

    def __str__(self):
        return (f"Patient: {self.patient}, Doctor: {self.slot.doctor}, Date: {self.slot.date}, "
                f"Start Time: {self.slot.start_time}, End Time: {self.slot.end_time}, Status: {self.status}")
