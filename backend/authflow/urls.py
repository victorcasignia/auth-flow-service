from django.urls import include, path, re_path
from rest_framework import routers
from dashboard_app import views
from rest_framework_simplejwt.views import TokenObtainSlidingView 
from dashboard_app.serializers import LoginJWTSerializer
from django.views.generic import TemplateView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      "API",
      default_version='v1',
      description="Documentation",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="victorcasignia@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register(r'api/users', views.UserViewSet)
router.register(r'api/roles', views.RoleViewSet)
router.register(r'api/permissions', views.PermissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/login/', TokenObtainSlidingView.as_view(serializer_class=LoginJWTSerializer), name='login'),
    path('api/signup/', views.SignupView.as_view(), name='signup'),
    path('api/roles/<int:id>/permissions', views.role_permissions, name='role_permissions'),
    path('api/users/<int:id>/roles', views.user_roles, name='user_roles'),
    path('api/users/<int:id>/permissions', views.user_permissions, name='user_permissions'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]