import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from .models import User


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            return self.get_response(request)

        auth_header = request.headers.get('Authorization')

        if auth_header:
            try:
                parts = auth_header.split(' ')
                if len(parts) == 2 and parts[0] == 'Bearer':
                    token = parts[1]
                    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                    user = User.objects.get(id=payload['user_id'], is_active=True)
                    request.user = user

            except Exception:
                request.user = AnonymousUser()

        else:
            request.user = AnonymousUser()

        return self.get_response(request)