from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Django Authentication API",
        default_version='v1',
        description="This API provides user authentication, profile management, and more.",
        contact=openapi.Contact(email="contact@authapi.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
from .views import (
    GetCSRFToken,
    CheckAuthenticatedView,
    RegistrationView,
    ActivateView,
    ActivationConfirm,
    LoginView,
    UserDetailView,
    ChangePasswordView,
    DeleteAccountView,
    LogoutView,
    ResetPasswordEmailView,
    ResetPasswordView,
    ResetPasswordConfirmView,
    ProfileView,
    
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('auth-api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('auth-api/get-csrf-token/', GetCSRFToken.as_view(), name='get_csrf_token'),
    path('auth-api/check-authenticated/', CheckAuthenticatedView.as_view(), name='check_authenticated'),
    path('auth-api/register/', RegistrationView.as_view(), name='register'),
    path('auth-api/activate/<str:uid>/<str:token>/', ActivateView.as_view(), name='activate'),
    path('auth-api/activate/confirm/', ActivationConfirm.as_view(), name='activation_confirm'),
    path('auth-api/login/', LoginView.as_view(), name='login'),
    path('auth-api/user-detail/', UserDetailView.as_view(), name='user_detail'),
    path('auth-api/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('auth-api/delete-account/', DeleteAccountView.as_view(), name='delete_account'),
    path('auth-api/logout/', LogoutView.as_view(), name='logout'),
    path('auth-api/reset-password-email/', ResetPasswordEmailView.as_view(), name='reset_password_email'),
    path('auth-api/reset-password/<str:uid>/<str:token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('auth-api/reset-password/confirm/', ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
    path('auth-api/profile/', ProfileView.as_view(), name='profile'),
]
