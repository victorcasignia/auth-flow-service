import email
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from dashboard_app.models import Permission, Role, ExtendedUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import SlidingToken
from dashboard_app.serializers import UserSerializer, RoleSerializer, PermissionSerializer, SignupSerializer
import json

class SignupViewTestCase(APITestCase):
    def test_create_account(self):
        url = reverse('signup')

        """Will not create user with missing email and password"""
        data = {'username': 'test'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 0)


        """Will not create user with missing email"""
        data = {'username': 'test', 'password': 'test123'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 0)

        """Will not create user with invalid email"""
        data = {'username': 'test', 'password': 'test123', 'email': 'email'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 0)

        """Will not create user with invalid username"""
        data = {'username': 1, 'password': 'test123', 'email': 'email'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 0)

        """Will not create user with password less than 6 characters"""
        data = {'username': 'test', 'password': '12345', 'email': 'email@email.com'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 0)

        """Will not create user with missing password2"""
        data = {'username': 'test', 'password': '12345a', 'email': 'email@email.com'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 0)

        """Will not create user with non-matching password2"""
        data = {'username': 'test', 'password': '12345a', 'password2': '12345b', 'email': 'email@email.com'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 0)

        """Will create user with valid fields"""
        data = {'username': 'test', 'password': '12345a', 'password2': '12345a', 'email': 'email@email.com'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_create_account_will_create_extended_user(self):
        url = reverse('signup')

        """Will create extended user object on user create"""

        self.assertEqual(ExtendedUser.objects.count(), 0)
        data = {'username': 'test', 'password': '12345a', 'password2': '12345a', 'email': 'email@email.com'}
        self.client.post(url, data, format='json')

        self.assertEqual(ExtendedUser.objects.count(), 1)
        user = get_user_model().objects.get(username='test')
        self.assertEqual(ExtendedUser.objects.first().user, user)

    def test_create_account_will_respond_with_profile(self):
        url = reverse('signup')

        """Will create extended user object on user create"""
        data = {'username': 'test', 'password': '12345a', 'password2': '12345a', 'email': 'email@email.com'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.content, b'{"username":"test","email":"email@email.com"}')

class UserIsCreatedTestCase(APITestCase):
    def setUp(self):
        url = reverse('signup')
        data = {'username': 'test', 'password': '12345a', 'password2': '12345a', 'email': 'email@email.com'}
        self.client.post(url, data, format='json')

        self.user = get_user_model().objects.get(username='test')

class LoginViewTestCase(UserIsCreatedTestCase):
    def setUp(self):
        super().setUp()

    def test_login(self):
        url = reverse('login')

        """Will not login with missing username"""
        data = {'password': '12345a'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """Will not login with missing password"""
        data = {'username': 'test'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """Will not login with unregistered user"""
        data = {'username': 'test2', 'password': '12345a'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """Will login with correct username"""
        data = {'username': 'test', 'password': '12345a'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_email(self):
        url = reverse('login')
        """Will login with email in username field"""
        data = {'username': 'email@email.com', 'password': '12345a'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_will_respond_with_jwt_token(self):
        url = reverse('login')
        """Will respond with jwt token and user id"""
        data = {'username': 'email@email.com', 'password': '12345a'}
        response = self.client.post(url, data, format='json')

        content = json.loads(response.content)
        self.assertTrue(content['access_token'])
        self.assertEqual(content['user_id'], self.user.id)

class Authenticated(UserIsCreatedTestCase):
    def setUp(self):
        super().setUp()
        self.token = str(SlidingToken.for_user(self.user))

        role = Role.objects.create(
            name='test'
        )
        role.save()
        permission = Permission.objects.create(
            name='test'
        )
        permission.save()

        self.role = role
        self.permission = permission


class AuthenticatedViewTestCase(Authenticated):
    def setUp(self):
        super().setUp()

    def test_protected_routes_need_authorization(self):
        protected_route_names_get = ['user-list', 'role-list', 'permission-list']
        protected_route_names_get_with_id = ['user_roles', 'user_permissions', 'role_permissions']
        protected_route_names_post = ['role-list', 'permission-list']
        protected_route_names_post_with_id = ['role_permissions', 'user_roles']

        """Will respond with unauthorized without credentials"""

        for name in protected_route_names_post:
            url = reverse(name)
            data = {'name': name }
            response = self.client.post(url, data, format='json')

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            response = self.client.post(url, data, format='json')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ')

        for name in protected_route_names_post_with_id:
            id = self.user.id if name.startswith('user') else self.role.id
            url = reverse(name, kwargs={'id': id})
            data = {'name': 'test' }
            response = self.client.post(url, data, format='json')

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            response = self.client.post(url, data, format='json')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ')

        for name in protected_route_names_get:
            url = reverse(name)
            data = {}

            response = self.client.get(url, data, format='json')

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            response = self.client.get(url, data, format='json')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ')

        for name in protected_route_names_get_with_id:
            id = self.user.id if name.startswith('user') else self.role.id
            url = reverse(name, kwargs={'id': id})
            data = {}
            response = self.client.get(url, data, format='json')

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
            response = self.client.get(url, data, format='json')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ')

class UserViewTestCase(Authenticated):
    def setUp(self):
        super().setUp()
    def test_can_view_users(self):
        url = reverse('user-list')
        """Will respond users"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url, format='json')

        content = json.loads(response.content)
        self.assertEqual(content, UserSerializer(get_user_model().objects.all(), many=True).data)

class RoleViewTestCase(Authenticated):
    def setUp(self):
        super().setUp()
    def test_can_view_roles(self):
        url = reverse('role-list')
        """Will respond roles"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url, format='json')

        content = json.loads(response.content)

        self.assertEqual(content, RoleSerializer(Role.objects.all(), many=True).data)

    def test_can_create_role(self):
        url = reverse('role-list')

        """Will note create role if it does not have name"""
        data = {'description': 'testrole'}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """Will create role if it has name"""
        data = {'name': 'testrole', 'description': 'description'}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class PermissionViewTestCase(Authenticated):
    def setUp(self):
        super().setUp()
    def test_can_view_permissions(self):
        url = reverse('permission-list')

        """Will respond permissions"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url, format='json')

        content = json.loads(response.content)

        self.assertEqual(content, PermissionSerializer(Permission.objects.all(), many=True).data)

    def test_can_create_permission(self):
        url = reverse('permission-list')

        """Will note create permission if it does not have name"""
        data = {'description': 'testpermission'}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """Will create permission if it has name"""
        data = {'name': 'testpermission', 'description': 'description'}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class UserRoleViewTestCase(Authenticated):
    def setUp(self):
        super().setUp()
        self.extended_user = ExtendedUser.objects.get(user_id=self.user.id)
        self.extended_user.roles.add(self.role)
        self.extended_user.save()

    def test_can_view_user_roles(self):
        url = reverse('user_roles', kwargs={'id': self.user.id})

        """Will respond roles"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url, format='json')

        content = json.loads(response.content)

        self.assertEqual(content, RoleSerializer(self.extended_user.roles, many=True).data)

    def test_can_add_user_roles(self):
        url = reverse('user_roles', kwargs={'id': self.user.id})

        new_role = Role.objects.create(
            name='new_role'
        )
        new_role.save()

        """Will add role"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.client.post(url, {'name': new_role.name}, format='json')

        self.assertTrue(self.extended_user.roles.get(id=new_role.id))

class RolePermissionViewTestCase(Authenticated):
    def setUp(self):
        super().setUp()
        self.role.permissions.add(self.permission)
        self.role.save()

    def test_can_view_role_permissions(self):
        url = reverse('role_permissions', kwargs={'id': self.role.id})

        """Will respond permissions"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url, format='json')

        content = json.loads(response.content)

        self.assertEqual(content, PermissionSerializer(self.role.permissions, many=True).data)

    def test_can_add_role_permissions(self):
        url = reverse('role_permissions', kwargs={'id': self.role.id})

        new_permission = Permission.objects.create(
            name='new_permission'
        )
        new_permission.save()

        """Will add permission"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.client.post(url, {'name': new_permission.name}, format='json')

        self.assertTrue(self.role.permissions.get(id=new_permission.id))

class UserPermissionViewTestCase(Authenticated):
    def setUp(self):
        super().setUp()

        self.extended_user = ExtendedUser.objects.get(user_id=self.user.id)
        self.extended_user.roles.add(self.role)
        self.extended_user.save()
        self.role.permissions.add(self.permission)
        self.role.save()

    def test_can_view_user_permissions(self):
        url = reverse('user_permissions', kwargs={'id': self.user.id})

        """Will respond permissions"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url, format='json')

        content = json.loads(response.content)

        permissions = []
        for role in self.extended_user.roles.all():
            permissions+=role.permissions.all()

        self.assertEqual(content, PermissionSerializer(permissions, many=True).data)