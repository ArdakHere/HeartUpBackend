from django.contrib import admin
from . import models


class HeartBeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'heart_beat_audio', 'heart_beat_audio_upload_on', 'patient_id')
    search_fields = ('heart_beat_audio', 'heart_beat_audio_upload_on')
    list_filter = ('heart_beat_audio_upload_on',)


class ECGAdmin(admin.ModelAdmin):
    list_display = ('id', 'ecg_file', 'ecg_file_upload_on', 'patient_id')
    search_fields = ('ecg_file', 'ecg_file_upload_on')
    list_filter = ('ecg_file_upload_on',)


class UCLAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_id', 'survival', 'age', 'pericardialeffusion', 'fractionalshortening', 'epss', 'lvdd', 'wallmotion_score', 'wallmotion_index', 'mult')
    search_fields = ('patient_id', 'survival', 'age', 'pericardialeffusion', 'fractionalshortening', 'epss', 'lvdd', 'wallmotion_score', 'wallmotion_index', 'mult')
    list_filter = ('survival', 'age', 'pericardialeffusion', 'fractionalshortening', 'epss', 'lvdd', 'wallmotion_score', 'wallmotion_index', 'mult')


class EchoNetAdmin(admin.ModelAdmin):
    list_display = ('id', 'echo_net_file', 'echo_net_file_upload_on', 'patient_id')
    search_fields = ('echo_net_file', 'echo_net_file_upload_on')
    list_filter = ('echo_net_file_upload_on',)


class MLDiagnosisAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_id', 'heart_beat_prediction', 'ecg_prediction', 'ucl_prediction', 'echo_net_prediction', 'heart_beat_prediction_on', 'ecg_prediction_on', 'ucl_prediction_on', 'echo_net_prediction_on')
    search_fields = ('patient_id', 'heart_beat_prediction', 'ecg_prediction', 'ucl_prediction', 'echo_net_prediction', 'heart_beat_prediction_on', 'ecg_prediction_on', 'ucl_prediction_on', 'echo_net_prediction_on')
    list_filter = ('heart_beat_prediction', 'ecg_prediction', 'ucl_prediction', 'echo_net_prediction', 'heart_beat_prediction_on', 'ecg_prediction_on', 'ucl_prediction_on', 'echo_net_prediction_on')


admin.site.register(models.HeartBeatModel, HeartBeatAdmin)
admin.site.register(models.ECGModel, ECGAdmin)
admin.site.register(models.UCLModel, UCLAdmin)
admin.site.register(models.EchoNetModel, EchoNetAdmin)
admin.site.register(models.MLDiagnosisModel, MLDiagnosisAdmin)
