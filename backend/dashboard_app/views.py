from dashboard_app.models import Role, Permission, ExtendedUser
from dashboard_app.serializers import UserSerializer, RoleSerializer, PermissionSerializer, SignupSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, generics, mixins
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

class UserViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset().filter(is_superuser=False)
        return qs


class RoleViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

class PermissionViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def role_permissions(request, id):
    role = Role.objects.get(pk=id)
    if request.method =='POST': 
        name = request.data.get('name')
        permission = Permission.objects.get(name=name)

        role.permissions.add(permission.id)

    return Response(PermissionSerializer(role.permissions, many=True).data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_roles(request, id):
    extended_user = ExtendedUser.objects.get(user_id=id)
    if request.method =='POST': 
        name = request.data.get('name')
        role = Role.objects.get(name=name)

        extended_user.roles.add(role.id)

    return Response(RoleSerializer(extended_user.roles, many=True).data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_permissions(request, id):
    extended_user = ExtendedUser.objects.get(user_id=id)

    permissions = []
    for role in extended_user.roles.all():
        permissions+=role.permissions.all()
    return Response(PermissionSerializer(permissions, many=True).data)