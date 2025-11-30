from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer

    def get(self, request):
        return Response({
            "message": "Форма регистрации",
            "instructions": "Заполните все поля для регистрации"
        })

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Пользователь успешно зарегистрирован',
                'user_id': user.id,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer

    def get(self, request):
        return Response({
            "message": "Форма входа",
            "instructions": "Введите email и пароль",
            "test_users": {
                "admin": "admin@example.com / admin123",
                "manager": "manager@example.com / manager123",
                "user": "user@example.com / user123"
            }
        })

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(email=email)
                if user.check_password(password) and user.is_active:
                    token = user.generate_jwt_token()
                    return Response({
                        'message': 'Успешный вход',
                        'token': token,
                        'user': UserProfileSerializer(user).data
                    })
                else:
                    return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({'error': 'Пользователь не найден'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        return Response({'message': 'Успешный выход'})


class UserProfileView(APIView):
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(APIView):
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({'message': 'Аккаунт успешно деактивирован'})