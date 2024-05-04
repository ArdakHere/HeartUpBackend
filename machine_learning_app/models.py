from django.db import models

from core_app import models as core_app_models


class HeartBeatModel(models.Model):
    patient = models.ForeignKey(core_app_models.Patient, on_delete=models.CASCADE)

    heart_beat_audio = models.FileField(upload_to='audio/')
    heart_beat_audio_upload_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.pk} {self.patient.user.first_name} {self.patient.user.last_name} "
                f"{self.patient.state_id} {self.heart_beat_audio_upload_on}")


class ECGModel(models.Model):
    patient = models.ForeignKey(core_app_models.Patient, on_delete=models.CASCADE)

    ecg_file = models.FileField(upload_to='ecg_files/')
    ecg_file_upload_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.pk} {self.patient.user.first_name} {self.patient.user.last_name} "
                f"{self.patient.state_id} {self.ecg_file_upload_on}")


class UCLModel(models.Model):
    patient = models.ForeignKey(core_app_models.Patient, on_delete=models.CASCADE)

    survival = models.PositiveIntegerField()
    age = models.PositiveIntegerField()
    pericardialeffusion = models.BooleanField()
    fractionalshortening = models.FloatField()
    epss = models.IntegerField()
    lvdd = models.IntegerField()
    wallmotion_score = models.IntegerField()
    wallmotion_index = models.FloatField()
    mult = models.FloatField()

    def __str__(self):
        return (f"{self.pk} {self.patient.user.first_name} {self.patient.user.last_name} "
                f"{self.patient.state_id} {self.survival} {self.age} {self.pericardialeffusion} "
                f"{self.fractionalshortening} {self.epss} {self.lvdd} {self.wallmotion_score} {self.wallmotion_index} "
                f"{self.mult}")


class EchoNetModel(models.Model):
    patient = models.ForeignKey(core_app_models.Patient, on_delete=models.CASCADE)

    echo_net_file = models.FileField(upload_to='echo_net_files/')
    echo_net_file_upload_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.pk} {self.patient.user.first_name} {self.patient.user.last_name} "
                f"{self.patient.state_id} {self.echo_net_file_upload_on}")


class MLDiagnosisModel(models.Model):
    patient = models.ForeignKey(core_app_models.Patient, on_delete=models.CASCADE)
    heart_beat = models.OneToOneField(HeartBeatModel, on_delete=models.CASCADE, blank=True, null=True)
    ecg = models.OneToOneField(ECGModel, on_delete=models.CASCADE, blank=True, null=True)
    ucl = models.OneToOneField(UCLModel, on_delete=models.CASCADE, blank=True, null=True)
    echo_net = models.OneToOneField(EchoNetModel, on_delete=models.CASCADE, blank=True, null=True)

    heart_beat_prediction = models.CharField(max_length=100, blank=True, null=True)
    ecg_prediction = models.CharField(max_length=100, blank=True, null=True)
    ucl_prediction = models.CharField(max_length=100, blank=True, null=True)
    echo_net_prediction = models.CharField(max_length=100, blank=True, null=True)

    heart_beat_prediction_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    ecg_prediction_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    ucl_prediction_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    echo_net_prediction_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return (f"{self.pk} {self.patient.user.first_name} {self.patient.user.last_name} {self.patient.state_id} "
                f"{self.heart_beat_prediction} {self.ecg_prediction} {self.ucl_prediction} {self.echo_net_prediction}")
