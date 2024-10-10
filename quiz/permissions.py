from rest_framework import permissions

class IsStudent(permissions.BasePermission):
    """
    Custom permission to only allow students to access the quiz endpoints.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has the student role
        return request.user.is_authenticated and request.user.role == 'Student'
