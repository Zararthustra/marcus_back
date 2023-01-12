from rest_framework.permissions import BasePermission

class MasterpiecePermission(BasePermission):
    def has_permission(self, request, view):
        # Write your permission logic here
        pass