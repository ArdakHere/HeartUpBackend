from rest_framework.permissions import BasePermission


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'patient'

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'patient'


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'doctor'

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'doctor'
