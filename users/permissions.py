from rest_framework import permissions

# Permission constants
VIEW_USERS = 'view_users'
CREATE_USERS = 'create_users'
UPDATE_USERS = 'update_users'
DELETE_USERS = 'delete_users'
MANAGE_ROLES = 'manage_roles'

ROLE_PERMISSIONS = {
    'Admin': {VIEW_USERS, CREATE_USERS, UPDATE_USERS, DELETE_USERS, MANAGE_ROLES},
    'Manager': {VIEW_USERS, CREATE_USERS, UPDATE_USERS},
    'User': set(),
}

class HasRBACPermission(permissions.BasePermission):
    """
    Checks if the user has the required RBAC permission for the action.
    """
    def has_permission(self, request, view):
        required_perm = getattr(view, 'required_permission', None)
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'Admin':
            return True
        if required_perm is None:
            return True
        return required_perm in ROLE_PERMISSIONS.get(request.user.role, set())

class IsSelfOrAdmin(permissions.BasePermission):
    """
    Allow users to access their own profile, or Admins to access any.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'Admin' or obj == request.user
