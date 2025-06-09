from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer, ChangeRoleSerializer
from .permissions import HasRBACPermission, IsSelfOrAdmin, VIEW_USERS, CREATE_USERS, UPDATE_USERS, DELETE_USERS, MANAGE_ROLES

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(username=request.data['username'])
            permissions_set = list(self.get_permissions_for_role(user.role))
            response.data['user'] = UserSerializer(user).data
            response.data['permissions'] = permissions_set
        return response

    def get_permissions_for_role(self, role):
        from .permissions import ROLE_PERMISSIONS
        if role == 'Admin':
            return [VIEW_USERS, CREATE_USERS, UPDATE_USERS, DELETE_USERS, MANAGE_ROLES]
        return list(ROLE_PERMISSIONS.get(role, []))

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [HasRBACPermission]
    required_permission = VIEW_USERS

    def get_queryset(self):
        user = self.request.user
        if user.role == 'User':
            return User.objects.filter(id=user.id)
        return User.objects.all()

class UserCreateView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [HasRBACPermission]
    required_permission = CREATE_USERS

class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [HasRBACPermission]
    required_permission = UPDATE_USERS

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [HasRBACPermission]
    required_permission = DELETE_USERS

class ChangeUserRoleView(APIView):
    permission_classes = [HasRBACPermission]
    required_permission = MANAGE_ROLES

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ChangeRoleSerializer(data=request.data)
        if serializer.is_valid():
            user.role = serializer.validated_data['role']
            user.save()
            return Response({'detail': 'Role updated.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
