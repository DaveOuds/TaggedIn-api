from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings

from contact.models import Contact
from django.conf import settings
from django.contrib.auth import (
    hashers as hashers
)
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from pymongo import MongoClient

from .app_settings import (
    TokenSerializer, JWTSerializer, RegisterSerializer,
    create_token, register_permission_classes
)

from .models import TokenModel
from .utils import jwt_encode


sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2', 'password1', 'password2'
    )
)
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = register_permission_classes()
    token_model = TokenModel

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def get_response_data(self, user):
        if allauth_settings.EMAIL_VERIFICATION == \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": _("Verification e-mail sent.")}

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': user,
                'token': self.token
            }
            return JWTSerializer(data).data
        else:
            return TokenSerializer(user.auth_token).data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(user)
        else:
            create_token(self.token_model, user, serializer)

        complete_signup(self.request._request, user,
                        allauth_settings.EMAIL_VERIFICATION,
                        None)
        return user


class DeleteUserView(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_owner(self, request):
        client = MongoClient('localhost', 27017)
        users = client.TaggedDB.auth_user
        user = users.find_one({"id": request.user.id})
        return str(user['_id'])

    def get_password(self, request):
        client = MongoClient('localhost', 27017)
        users = client.TaggedDB.auth_user
        user = users.find_one({"id": request.user.id})
        return str(user['password'])

    def get(self, request):
        owner = self.get_owner(request)
        contacts = Contact.objects.all().filter(owner=owner)
        contacts.delete()
        request.user.delete()
        return Response("User deleted.", status=204)

    def post(self, request):
        if hashers.check_password(request.data.get('password'), self.get_password(request)):
            owner = self.get_owner(request)
            contacts = Contact.objects.all().filter(owner=owner)
            contacts.delete()
            request.user.delete()
            return Response("", status=204)
        else:
            return Response("", status=500)