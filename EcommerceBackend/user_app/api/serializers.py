from rest_framework import serializers
from ..models import User  # CustomUser, Address
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
from django.contrib.auth.hashers import make_password


# class AddressSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Address
#         fields = '__all__'

#     def update(self, instance, validated_data):
#         instance.street = validated_data.get('street', instance.street)
#         instance.city = validated_data.get('city', instance.city)
#         instance.country = validated_data.get('country', instance.country)
#         instance.building_number = validated_data.get(
#             'building_number', instance.building_number)
#         instance.save()
#         return instance

# , 'addresses'
class UserSerializer(serializers.ModelSerializer):
    # addresses = AddressSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'phone', 'date_of_birth']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }

    def create(self, validated_data):

        validated_data['is_active'] = True
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise ValidationError('This email is already exists!')

        if 'phone' not in data:
            # Handle missing phone number
            raise serializers.ValidationError('Phone number is required.')

        if User.objects.filter(phone=data['phone']).exists():
            raise serializers.ValidationError('Phone number already exists.')

        if data['password'] != data['confirm_password']:
            raise ValidationError("Passwords don't match")

        return data

    def to_representation(self, instance):
        if isinstance(instance, get_user_model()):
            return super().to_representation(instance)
        else:
            # Handle anonymous user
            return {'id': None, 'username': 'Anonymous', 'email': None}


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'error': 'P1 and P2 should be same!'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError(
                {'error': 'Email already exists!'})

        account = User(
            email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()

        return account


# class UserUpdateSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(required=False)
#     phone = serializers.CharField(required=False)
#     # image=CloudinaryField()
#     password = serializers.CharField(required=False, write_only=True)
#     confirm_password = serializers.CharField(required=False, write_only=True)
#     # addresses = AddressSerializer(many=True)

#     class Meta:
#         model = User
#         fields = ['email', 'username', 'password',
#                   'confirm_password', 'phone', 'date_of_birth']

#     def validate(self, attrs):
#         if not any(attrs.values()):
#             raise serializers.ValidationError(
#                 "At least one field must be updated")

#         password = attrs.get('password')
#         confirm_password = attrs.get('confirm_password')
#         if not password or not confirm_password or password != confirm_password:
#             raise serializers.ValidationError
#         return attrs

#     def update(self, instance, validated_data):
#         password = validated_data.pop('password', None)
#         confirm_password = validated_data.pop('confirm_password', None)
#         # addresses_data = validated_data.pop('addresses', [])

#         if password and confirm_password:
#             validated_data['password'] = make_password(password)
#             validated_data['confirm_password'] = make_password(
#                 confirm_password)

#         instance = super().update(instance, validated_data)

#         # for address_data in addresses_data:
#         #     address_id = address_data.get('id', None)
#         #     if address_id:
#         #         try:
#         #             address = Address.objects.get(id=address_id, user=instance)
#         #             address_serializer = AddressSerializer(
#         #                 address, data=address_data)
#         #             if address_serializer.is_valid():
#         #                 address_serializer.save()
#         #             else:
#         #                 raise serializers.ValidationError(
#         #                     address_serializer.errors)
#         #         except Address.DoesNotExist:
#         #             raise serializers.ValidationError(
#         #                 f"Address with id {address_id} does not exist.")
#         #     else:
#         #         address_serializer = AddressSerializer(data=address_data)
#         #         if address_serializer.is_valid():
#         #             address_serializer.save(user=instance)
#         #         else:
#         #             raise serializers.ValidationError(
#         #                 address_serializer.errors)

#         return instance
