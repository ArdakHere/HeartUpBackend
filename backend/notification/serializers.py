from rest_framework import serializers
from . import models


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NotificationModel
        fields = '__all__'
