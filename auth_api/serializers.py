from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers
from auth_api.models import User, Profile
import re

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Handles user creation, update, and validation.
    """

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "confirm_password"]

    def validate(self, attrs):
        """
        Custom validation to ensure that password and confirm_password match.
        """
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Password and Confirm Password don't match.")
        return attrs
    
    def validate_email(self, value):
        """
        Custom validation to check if a user with the given email already exists.
        Also, checks if the email format is valid.
        """
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError('Enter a valid email address.')

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        
        return value
    
    def create(self, validated_data):
        """
        Custom create method to handle user creation.
        """
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        user.is_active = False
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """
        Custom update method to handle user updates.
        """
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.

    Handles profile creation, update, and validation.
    """

    class Meta:
        model = Profile
        fields = ['mobile', 'location', 'dob', 'bio', 'gender', 'avatar']

    def validate_mobile(self, value):
        """
        Custom validation to check if the mobile number is valid using regular expression.
        """
        # Example: Check if the mobile number has a valid format (10 digits)
        if not re.fullmatch(r'^[6-9]\d{9}$', value):
            raise serializers.ValidationError('Invalid mobile number format. Please enter a 10-digit number.')

        return value

    def create(self, validated_data):
        """
        Custom create method to handle profile creation.
        """
        user = self.context['request'].user
        profile = Profile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        """
        Custom update method to handle profile updates.
        """
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.location = validated_data.get('location', instance.location)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance
