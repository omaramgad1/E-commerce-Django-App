from django.forms import ValidationError
from rest_framework import serializers
from ..models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password


class RegistrationSerializer(serializers.ModelSerializer):
    # We are writing this becoz we need confirm password field in our Registratin Request
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'phone', 'date_of_birth',
                  'profileImgUrl', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match")
            # Custom password validation
        if len(password) < 8:
            raise serializers.ValidationError(
                {"password": "Password must be at least 8 characters long."})

        if password.isnumeric():
            raise serializers.ValidationError(
                {"password": "Password cannot contain only numeric characters."})

        return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True, style={
                                     'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()

            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return {
                    'is_admin': user.is_superuser,
                    'token': str(refresh.access_token),

                    # 'access_token': str(refresh.access_token),
                    # 'refresh_token': str(refresh),
                }
            else:
                raise serializers.ValidationError(
                    "Unable to authenticate with provided credentials")
        else:
            raise serializers.ValidationError(
                "Email and password are required")


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_of_birth', 'phone', 'profileImgUrl')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'date_of_birth', 'phone', 'profileImgUrl')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'})
    confirm_new_password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs


# class ForgotPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate(self, attrs):
#         email = attrs['email']
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             raise serializers.ValidationError('User not found')
#         attrs['user'] = user
#         return attrs


# class ResetPasswordSerializer(serializers.Serializer):
#     new_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
#     confirm_new_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

#     def validate(self, attrs):
#         if attrs['new_password'] != attrs['confirm_new_password']:
#             raise serializers.ValidationError("New passwords don't match")
#         return attrs# class UserChangePasswordSerializer(serializers.Serializer):
