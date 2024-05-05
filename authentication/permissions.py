from rest_framework import permissions


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'DOCTOR') or request.user.role == 'ADMIN'


class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'PATIENT') or request.user.role == 'ADMIN'


class IsDoctorOrIsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'DOCTOR' or request.user.role == 'PATIENT' or request.user.role == 'ADMIN'


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'USER') or request.user.role == 'ADMIN'


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CanWriteIfOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CanWriteIfAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'ADMIN'

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'ADMIN'


class CanWriteIfOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'ADMIN'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.role == 'ADMIN'


class CanWriteIfDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'DOCTOR' or request.user.role == 'ADMIN'

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'DOCTOR' or request.user.role == 'ADMIN'
