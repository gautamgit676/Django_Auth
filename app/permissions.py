from rest_framework.permissions import BasePermission, SAFE_METHODS

class UserRolePermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        # Admins can do anything
        if user.user_role == 'admin':
            return True

        # Managers can create and update, not delete
        if user.user_role == 'manager':
            if request.method in ['POST', 'PUT', 'PATCH', 'GET']:
                return True
            return False  # No DELETE for managers

        # Employees can only view (GET)
        if user.user_role == 'employee':
            if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
                return True
            return False
        return False  