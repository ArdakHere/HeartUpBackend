from rest_framework import serializers

from . import models


class PatientSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = models.Patient
        fields = ('id', 'state_id', 'photo', 'age', 'dob', 'sex', 'height', 'weight',
                  'user', 'first_name', 'last_name', 'email', 'role')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        ret['photo'] = request.build_absolute_uri(ret['photo'])
        return ret


class DoctorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = models.Doctor
        fields = ('id', 'photo', 'phone', 'specialization', 'aboutme', 'work_location',
                  'user', 'first_name', 'last_name', 'email', 'role')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        ret['photo'] = request.build_absolute_uri(ret['photo'])
        return ret
