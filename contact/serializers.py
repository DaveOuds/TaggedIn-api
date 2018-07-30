from rest_framework import serializers
from contact.models import Contact
from django.contrib.auth.models import User


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('_id', 'name', 'emailAddress', 'company', 'position', 'connectedOn', 'tags', 'owner')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('_id', 'username', 'snippets')