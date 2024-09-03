from rest_framework import permissions


class CustomDoctorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.role in ['ADMIN', 'DOCTOR']

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return request.user.role in ['ADMIN',] or obj.user == request.user


class CustomPatientPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.role in ['ADMIN']

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user.role in ['ADMIN', 'DOCTOR'] or obj.user == request.user
        return request.user.role in ['ADMIN',] or obj.user == request.user