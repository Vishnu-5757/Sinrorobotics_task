# tasks/permissions.py
from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superadmin()

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()

class IsAssignedUserOrAdmin(permissions.BasePermission):
    """
    Allows access if the user is the assigned user or an admin/superadmin.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_superadmin() or request.user.is_admin():
            return True
        return obj.assigned_to_id == request.user.id
