from rest_framework import permissions


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_doctor)

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_doctor)


class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_patient)

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_patient)


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_user)

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_user)
