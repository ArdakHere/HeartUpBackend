from django.db import models
from core_app import models as core_models


class Medication(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.pk} {self.name} {self.description}"


class Prescription(models.Model):
    appointment_id = models.ForeignKey(core_models.Appointment, on_delete=models.CASCADE)
    medication_id = models.ForeignKey(Medication, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(core_models.Doctor, on_delete=models.CASCADE)
    patient_id = models.ForeignKey(core_models.Patient, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.pk} {self.appointment_id} {self.medication_id} {self.doctor_id} {self.patient_id} {self.date}"


class Diagnosis(models.Model):
    appointment_id = models.ForeignKey(core_models.Appointment, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(core_models.Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    code = models.CharField(max_length=10)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.pk} {self.appointment_id} {self.doctor_id} {self.code} {self.date} {self.notes}"


class MedicalImage(models.Model):
    IMAGE_TYPE = (
        ('x-ray', 'x-ray'),
        ('mri', 'mri'),
        ('ct-scan', 'ct-scan'),
        ('ultrasound', 'ultrasound'),
        ('pet-scan', 'pet-scan'),
        ('ecg', 'ecg'),
        ('eeg', 'eeg'),
        ('ekg', 'ekg'),
        ('colonoscopy', 'colonoscopy'),
        ('endoscopy', 'endoscopy'),
        ('laparoscopy', 'laparoscopy'),
        ('angiography', 'angiography'),
        ('mammography', 'mammography'),
        ('biopsy', 'biopsy'),
        ('blood-test', 'blood-test'),
        ('urine-test', 'urine-test'),
        ('stool-test', 'stool-test'),
        ('sputum-test', 'sputum-test'),
        ('biopsy', 'biopsy'),
        ('bone-scan', 'bone-scan'),
        ('doppler', 'doppler'),
        ('echo', 'echo'),
        ('ekg', 'ekg'),
        ('emg', 'emg'),
        ('endoscopy', 'endoscopy'),
        ('fluoroscopy', 'fluoroscopy'),
        ('mammography', 'mammography'),
        ('pet-scan', 'pet-scan'),
        ('ultrasound', 'ultrasound'),
        ('x-ray', 'x-ray'),
    )
    patient_id = models.ForeignKey(core_models.Patient, on_delete=models.CASCADE)
    appointment_id = models.ForeignKey(core_models.Appointment, on_delete=models.CASCADE)
    image_type = models.CharField(max_length=100, choices=IMAGE_TYPE)
    image = models.ImageField(upload_to='medical_images/')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.pk} {self.patient_id} {self.appointment_id} {self.image_type} {self.image} {self.description}"
