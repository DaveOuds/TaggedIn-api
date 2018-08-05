from contact.models import Contact
from django.contrib.auth import hashers

from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2', 'password1', 'password2'
    )
)
class DeleteUserView(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_password(self, request):
        user = User.objects.get(username__exact= request.user.username)
        return user.password

    def get(self, request):
        current_user = request.user
        owner = current_user.id
        contacts = Contact.objects.all().filter(owner=owner)
        contacts.delete()
        request.user.delete()
        return Response("User deleted.", status=204)

    def post(self, request):
        if hashers.check_password(request.data.get('password'), self.get_password(request)):
            username = request.user.username
            u = User.objects.get(username=username)
            contacts = Contact.objects.all().filter(owner=username)
            contacts.delete()
            u.delete()
            return Response("", status=204)
        else:
            return Response("", status=500)