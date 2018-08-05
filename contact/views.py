from contact.models import Contact
from contact.serializers import ContactSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


@permission_classes((IsAuthenticated, ))
class ContactList(APIView):
    def get(self, request):
        owner = request.user.username
        contacts = Contact.objects.filter(owner=owner)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        owner = request.user.username
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
        owner = request.user.username
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