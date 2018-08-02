from contact.models import Contact
from contact.serializers import ContactSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from pymongo import MongoClient


@permission_classes((IsAuthenticated, ))
class ContactList(APIView):
    def get_owner(self, request):
        client = MongoClient('localhost', 27017)
        users = client.TaggedDB.auth_user
        user = users.find_one({"id": request.user.id})
        return str(user['_id'])

    def get(self, request):
        owner = self.get_owner(request)
        contacts = Contact.objects.filter(owner=owner)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        owner = self.get_owner(request)
        contacts = Contact.objects.all().filter(owner=owner)
        contacts.delete
        for contact in request.data:
           contact['owner'] = owner
        serializer = ContactSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        owner = self.get_owner(request)
        contacts = Contact.objects.filter(owner=owner)
        contacts.delete()
        return Response("All data deleted", status=200)


@api_view(['GET', 'PUT', 'DELETE', 'POST'])
@permission_classes((IsAuthenticated, ))
def contact_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        contact = Contact.objects.get(pk=pk)
    except Contact.DoesNotExist:
        return Response(status=404)

    client = MongoClient('localhost', 27017)
    users = client.TaggedDB.auth_user
    user = users.find_one({"id": request.user.id})
    user_id = str(user['_id'])

    if user_id != contact.owner:
        return Response("You are not authorized for this data.", status=402)

    if request.method == 'GET':
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        contact.delete()
        return Response(status=204)

    elif request.method == 'POST':
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)