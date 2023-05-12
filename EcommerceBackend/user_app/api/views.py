from rest_framework import status
from ..models import User
from .serializers import RegistrationSerializer, LoginSerializer, UserProfileSerializer, UserUpdateSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.paginator import Paginator


# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            response = serializer.validated_data
            response['message'] = 'Login successful'
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_get(request):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profile_update(request):
    user = request.user
    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        old_password = serializer.validated_data['old_password']
        if not user.check_password(old_password):
            return Response({'error': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'msg': 'Password changed successfully'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_active_users(request):
    users = User.objects.filter(is_active=True)
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users_pagination(request):
    if request.method == 'GET':
        queryset = User.objects.all()
        queryset_len = User.objects.all().count()
        limit = request.GET.get('limit', 10)
        page = request.GET.get('page', 1)

        paginator = Paginator(queryset, limit)
        objects = paginator.get_page(page)
        serializer = UserProfileSerializer(objects, many=True)
        return Response({'data': serializer.data,
                         'previous_page': objects.previous_page_number() if objects.has_previous() else None,
                         'current_page': objects.number,
                         'next_page': objects.next_page_number() if objects.has_next() else None,
                         'total_Docs': queryset_len,
                         'total_pages': paginator.num_pages,
                         })


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def change_user_active_status(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    is_active = request.data.get('is_active', None)
    if is_active is not None:
        user.is_active = is_active
        user.save()
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'is_active field is required'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def change_user_superuser_status(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    is_superuser = request.data.get('is_superuser', None)
    if is_superuser is not None:
        user.is_superuser = is_superuser
        user.save()
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'is_superuser field is required'}, status=status.HTTP_400_BAD_REQUEST)


# def get_user_by_token(request):
#     token = request.COOKIES.get('jwt')
#     if token:
#         try:
#             payload = RefreshToken(token).payload
#             user_id = payload.get('user_id')
#             user = User.objects.get(id=user_id)
#             return user
#         except User.DoesNotExist:
#             pass
#     return None

# def get_user_profile(request):
#     user = get_user_by_token(request)
#     if user:
#         serializer = UserProfileSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response({'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

# @api_view(['POST'])
# def forgot_password(request):
#     serializer = ForgotPasswordSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.validated_data['user']
#         token = RefreshToken.for_user(user)
#         email_body = f'Use this token to reset your password: {token}'
#         send_mail(
#             'Password reset token',
#             email_body,
#             'from@example.com',
#             [user.email],
#             fail_silently=False,
#         )
#         return Response({'msg': 'Password reset email sent'}, status=status.HTTP_200_OK)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def reset_password(request):
#     token = request.data.get('token', '')
#     serializer = ResetPasswordSerializer(data=request.data)
#     if serializer.is_valid():
#         try:
#             payload = jwt.decode(
#                 token, settings.SECRET_KEY, algorithms=['HS256'])
#             user_id = payload['user_id']
#             user = User.objects.get(id=user_id)
#         except (jwt.exceptions.DecodeError, User.DoesNotExist):
#             return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

#         user.set_password(serializer.validated_data['new_password'])
#         user.save()
#         return Response({'msg': 'Password reset successful'}, status=status.HTTP_200_OK)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
