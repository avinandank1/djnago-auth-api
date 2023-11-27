from django.contrib.auth import authenticate, login, logout
from auth_api.models import User, Profile
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from auth_api.serializers import UserSerializer, ProfileSerializer
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.conf import settings
from auth_api.utils import send_activation_email, send_reset_password_email




@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Get CSRF token for the user.
        """
        try:
            return Response({'success': 'CSRF Cookie set Successfully'})
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_protect, name='dispatch')
class CheckAuthenticatedView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Check if the user is authenticated.
        """
        try:
            if request.user.is_authenticated:
                return Response({'isAuthenticated': True})
            else:
                return Response({'isAuthenticated': False})
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_protect, name='dispatch')
class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle user registration.
        """
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.create(serializer.validated_data)

                # Send Account Activation Email
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                activation_link = reverse('activate', kwargs={'uid': uid, 'token': token})
                activation_url = f'{settings.SITE_DOMAIN}{activation_link}'
                send_activation_email(user.email, activation_url)

                return Response({'detail': 'Registration successful. Please Cheak your email Activation email sent.'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_protect, name='dispatch')
class ActivateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Confirm user activation.
        """
        try:
            uid = request.data.get('uid')
            token = request.data.get('token')
            if not uid or not token:
                return Response({'detail': 'Missing uid or token.'}, status=status.HTTP_400_BAD_REQUEST)

            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                if user.is_active:
                    return Response({'detail': 'Account is already activated.'}, status=status.HTTP_200_OK)

                user.is_active = True
                user.save()
                return Response({'detail': 'Account activated successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_protect, name='dispatch')
class ActivationConfirm(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Confirm user activation.
        """
        try:
            uid = request.data.get('uid')
            token = request.data.get('token')
            if not uid or not token:
                return Response({'detail': 'Missing uid or token.'}, status=status.HTTP_400_BAD_REQUEST)

            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                if user.is_active:
                    return Response({'detail': 'Account is already activated.'}, status=status.HTTP_200_OK)

                user.is_active = True
                user.save()
                return Response({'detail': 'Account activated successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle user login.
        """
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return Response({'detail': 'Logged in successfully.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Account is not activated.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Email or Password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDetailView(APIView):
    """
    Get and update user details.
    """

    def get(self, request):
        """
        Get user details.
        """
        try:
            serializer = UserSerializer(request.user)
            data = serializer.data
            data['is_staff'] = request.user.is_staff
            return Response(data)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        """
        Update user details.
        """
        try:
            serializer = UserSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChangePasswordView(APIView):
    """
    Change user password.
    """

    def post(self, request):
        """
        Change user password.
        """
        try:
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')
            user = request.user

            if not user.check_password(old_password):
                return Response({'detail': 'Invalid old password.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteAccountView(APIView):
    """
    Delete user account.
    """

    def delete(self, request):
        """
        Delete user account.
        """
        try:
            user = request.user
            user.delete()
            logout(request)
            return Response({'detail': 'Account deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_protect, name='dispatch')
class LogoutView(APIView):
    """
    Logout user.
    """

    def post(self, request):
        """
        Handle user logout.
        """
        try:
            logout(request)
            return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_protect, name='dispatch')
class ResetPasswordEmailView(APIView):
    """
    View to send a password reset email.

    This view expects a POST request with the user's email.
    It generates a password reset token, creates a reset link, and sends it to the user's email.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Send password reset email.
        """
        try:
            email = request.data.get('email')

            if not User.objects.filter(email=email).exists():
                return Response({'detail': 'User with this email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(email=email)

            # Generate password reset token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = reverse('reset_password', kwargs={'uid': uid, 'token': token})
            reset_url = f'{settings.SITE_DOMAIN}{reset_link}'
            send_reset_password_email(user.email, reset_url)

            return Response({'detail': 'Password reset email sent successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_protect, name='dispatch')
class ResetPasswordView(APIView):
    """
    Placeholder view for the password reset link.

    """
    permission_classes = [AllowAny]


@method_decorator(csrf_protect, name='dispatch')
class ResetPasswordConfirmView(APIView):
    """
    View to confirm a password reset.

    Expects a POST request with 'uid', 'token', and 'new_password' in the request data.
    If the reset link is valid, it updates the user's password.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Confirm password reset.
        """
        try:
            uid = request.data.get('uid')
            token = request.data.get('token')
            if not uid or not token:
                return Response({'detail': 'Missing uid or token.'}, status=status.HTTP_400_BAD_REQUEST)

            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                new_password = request.data.get('new_password')

                if not new_password:
                    return Response({'detail': 'New password is required.'}, status=status.HTTP_400_BAD_REQUEST)

                user.set_password(new_password)
                user.save()
                return Response({'detail': 'Password reset successful.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid reset password link.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid reset password link.'}, status=status.HTTP_400_BAD_REQUEST)



@method_decorator(csrf_protect, name='dispatch')
class ProfileView(APIView):
    """
    View to handle profile creation, retrieval, update, and deletion.

    Requires the user to be authenticated.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve the profile of the authenticated user.
        """
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({'detail': 'Profile does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """
        Create a new profile for the authenticated user.
        """
        try:
            serializer = ProfileSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        """
        Update the profile of the authenticated user.
        """
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({'detail': 'Profile does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        

    def delete(self, request):
        """
        Delete the profile of the authenticated user.
        """
        try:
            profile = Profile.objects.get(user=request.user)
            profile.delete()
            return Response({'detail': 'Profile deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Profile.DoesNotExist:
            return Response({'detail': 'Profile does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
