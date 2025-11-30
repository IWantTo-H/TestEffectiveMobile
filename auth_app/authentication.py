from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            # Format: "Bearer <token>"
            parts = auth_header.split(' ')
            if len(parts) != 2 or parts[0] != 'Bearer':
                return None

            token = parts[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'], is_active=True)
            return (user, token)

        except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError, User.DoesNotExist):
            return None