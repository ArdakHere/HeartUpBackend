from django.db import models


class AppointmentModel(models.Model):
    STATUS = (
        ('PENDING', 'PENDING'),
        ('APPROVED', 'APPROVED'),
        ('REJECTED', 'REJECTED')
    )

    patient = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='appointment_requests')
    doctor = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='appointment_requests')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(choices=STATUS, default='PENDING')

    def __str__(self):
        return (f"Patient: {self.patient}, Doctor: {self.doctor}, Date: {self.date}, "
                f"Start Time: {self.start_time}, End Time: {self.end_time}, Status: {self.status}")

    def save(self, *args, **kwargs):
        if self.start_time >= self.end_time:
            raise ValueError("Start time must be less than end time")
        super().save(*args, **kwargs)

