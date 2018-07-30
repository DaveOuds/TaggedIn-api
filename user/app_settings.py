from django.conf import settings

from rest_framework.permissions import AllowAny
from user.serializers import (
    TokenSerializer as DefaultTokenSerializer,
    JWTSerializer as DefaultJWTSerializer,
    LoginSerializer as DefaultLoginSerializer,
    RegisterSerializer as DefaultRegisterSerializer
)

from .utils import import_callable, default_create_token

create_token = import_callable(
    getattr(settings, 'REST_AUTH_TOKEN_CREATOR', default_create_token))

serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})

TokenSerializer = import_callable(
    serializers.get('TOKEN_SERIALIZER', DefaultTokenSerializer))

JWTSerializer = import_callable(
    serializers.get('JWT_SERIALIZER', DefaultJWTSerializer))

LoginSerializer = import_callable(
    serializers.get('LOGIN_SERIALIZER', DefaultLoginSerializer)
)

RegisterSerializer = import_callable(
    serializers.get('REGISTER_SERIALIZER', DefaultRegisterSerializer))

def register_permission_classes():
    permission_classes = [AllowAny, ]
    for klass in getattr(settings, 'REST_AUTH_REGISTER_PERMISSION_CLASSES', tuple()):
        permission_classes.append(import_callable(klass))
    return tuple(permission_classes)