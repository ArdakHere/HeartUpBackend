import json
import os

from dotenv import load_dotenv
from rest_framework import generics, status, permissions
import requests
from rest_framework.response import Response

from heartUpBackend.settings import BASE_DIR
from . import models
from . import serializer

load_dotenv(BASE_DIR / ".env")

HEARBEAT_API = os.getenv('API_HEART_BEAT_URL')
ECG_API = os.getenv('API_ECG_URL')
UCL_API = os.getenv('API_UCL_URL')
ECHONET_API = os.getenv('API_ECHONET_URL')


class HeartBeatView(generics.ListAPIView):
    queryset = models.HeartBeatModel.objects.all()
    serializer_class = serializer.HeartBeatSerializer


class ECGView(generics.ListAPIView):
    queryset = models.ECGModel.objects.all()
    serializer_class = serializer.ECGSerializer


class UCLView(generics.ListAPIView):
    queryset = models.UCLModel.objects.all()
    serializer_class = serializer.UCLSerializer


class EchoNetView(generics.ListAPIView):
    queryset = models.EchoNetModel.objects.all()
    serializer_class = serializer.EchoNetSerializer


class MLDiagnosisView(generics.ListCreateAPIView):
    queryset = models.MLDiagnosisModel.objects.all()
    serializer_class = serializer.MLDiagnosisSerializer

    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        print("=============")
        print("REQUEST:", request.data)
        try:
            serializer_instance = serializer.MLDiagnosisSerializer(data=request.data)
            if serializer_instance.is_valid(raise_exception=False):
                pass
            else:
                return Response({'error': serializer_instance.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)

        heart_beat_audio = request.data['heart_beat.heart_beat_audio']
        ecg_file = request.data['ecg.ecg_file']
        echo_net_file = request.data['echo_net.echo_net_file']
        ucl_survival = request.data['ucl.survival']
        ucl_age = request.data['ucl.age']
        ucl_pericardialeffusion = request.data.get('ucl.pericardialeffusion', False)
        if ucl_pericardialeffusion:
            ucl_pericardialeffusion = ucl_pericardialeffusion.lower() == 'true'
        ucl_fractionalshortening = request.data['ucl.fractionalshortening']
        ucl_epss = request.data['ucl.epss']
        ucl_lvdd = request.data['ucl.lvdd']
        ucl_wallmotion_score = request.data['ucl.wallmotion_score']
        ucl_wallmotion_index = request.data['ucl.wallmotion_index']
        ucl_mult = request.data['ucl.mult']

        patient_id = request.data['patient']

        heart_beat = models.HeartBeatModel.objects.create(
            patient_id=patient_id,
            heart_beat_audio=heart_beat_audio
        )

        heart_beat_audio_path = heart_beat.heart_beat_audio.path

        ecg = models.ECGModel.objects.create(
            patient_id=patient_id,
            ecg_file=ecg_file
        )

        ecg_file_path = ecg.ecg_file.path

        echo_net = models.EchoNetModel.objects.create(
            patient_id=patient_id,
            echo_net_file=echo_net_file
        )

        echo_net_path = echo_net.echo_net_file.path

        ucl = models.UCLModel.objects.create(
            patient_id=patient_id,
            survival=ucl_survival,
            age=ucl_age,
            pericardialeffusion=ucl_pericardialeffusion,
            fractionalshortening=ucl_fractionalshortening,
            epss=ucl_epss,
            lvdd=ucl_lvdd,
            wallmotion_score=ucl_wallmotion_score,
            wallmotion_index=ucl_wallmotion_index,
            mult=ucl_mult
        )

        try:
            with open(heart_beat_audio_path, 'rb') as heart_beat_audio:
                heart_beat_response = requests.post(
                    HEARBEAT_API,
                    files={'file': heart_beat_audio.read()}
                )

            with open(ecg_file_path, 'rb') as file:
                ecg_response = requests.post(
                    ECG_API,
                    files={'files': file}
                )

            with open(echo_net_path, 'rb') as file:
                echo_net_response = requests.post(
                    ECHONET_API,
                    files={'file': file}
                )

            ucl_response = requests.post(
                UCL_API,
                data=json.dumps({
                    'survival': ucl_survival,
                    'age': ucl_age,
                    'pericardialeffusion': ucl_pericardialeffusion,
                    'fractionalshortening': ucl_fractionalshortening,
                    'epss': ucl_epss,
                    'lvdd': ucl_lvdd,
                    'wallmotion_score': ucl_wallmotion_score,
                    'wallmotion_index': ucl_wallmotion_index,
                    'mult': ucl_mult
                }),
                headers={'Content-Type': 'application/json'}
            )

            if heart_beat_response.status_code != status.HTTP_200_OK or \
                    ecg_response.status_code != status.HTTP_200_OK or \
                    ucl_response.status_code != status.HTTP_200_OK:
                heart_beat.heart_beat_audio.delete()
                heart_beat.delete()
                ecg.ecg_file.delete()
                ecg.delete()
                echo_net.echo_net_file.delete()
                echo_net.delete()
                ucl.delete()
                return Response({'error': 'An error occurred while processing the request'},
                                status=status.HTTP_400_BAD_REQUEST)

            heart_beat_prediction = heart_beat_response.json()['prediction']
            ecg_prediction = ecg_response.json()['class']
            ucl_prediction = ucl_response.json()['prediction']
            echo_net_prediction = echo_net_response.json()
        except requests.exceptions.RequestException as e:
            heart_beat.heart_beat_audio.delete()
            heart_beat.delete()
            ecg.ecg_file.delete()
            ecg.delete()
            echo_net.echo_net_file.delete()
            echo_net.delete()
            ucl.delete()
            return Response({'error': 'An error occurred while processing the request'},
                            status=status.HTTP_400_BAD_REQUEST)

        ml_diagnosis = models.MLDiagnosisModel.objects.create(
            patient_id=patient_id,
            heart_beat=heart_beat,
            ecg=ecg,
            ucl=ucl,
            echo_net=echo_net,
            heart_beat_prediction=heart_beat_prediction,
            ecg_prediction=ecg_prediction,
            ucl_prediction=ucl_prediction,
            echo_net_prediction=echo_net_prediction,
        )

        ml_diagnosis_serializer = self.get_serializer(ml_diagnosis)
        return Response(ml_diagnosis_serializer.data, status=status.HTTP_201_CREATED)


class MLDiagnosisDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MLDiagnosisModel.objects.all()
    serializer_class = serializer.MLDiagnosisSerializer


class MLDiagnosisDetailByPatientView(generics.ListAPIView):
    serializer_class = serializer.MLDiagnosisSerializer

    def get_queryset(self):
        patient_id = self.kwargs['patient']
        return models.MLDiagnosisModel.objects.filter(patient_id=patient_id)
