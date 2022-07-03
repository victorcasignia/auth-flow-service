from django.db import models
from django.contrib.auth import get_user_model

class Permission(models.Model):
    name = models.CharField(max_length = 255, unique=True)
    description = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'dashboard_app'


class Role(models.Model):
    name = models.CharField(max_length = 255, unique=True)
    description = models.TextField(default='')
    permissions = models.ManyToManyField(Permission, related_name='roles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'dashboard_app'

class ExtendedUser(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    roles = models.ManyToManyField(Role, related_name='roles')

    class Meta:
        app_label = 'dashboard_app'
