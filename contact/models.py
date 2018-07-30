from django.db import models
from djongo import models as djodels

def number():
    no = Contact.objects.count()
    if no == None:
        return 1
    else:
        return no + 1

class Contact(models.Model):
    _id = models.IntegerField(primary_key=True, default=number)
    name = models.CharField(max_length=50)
    emailAddress = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    position = models.CharField(max_length=250, blank=True)
    connectedOn = models.CharField(max_length=50)
    tags = djodels.ListField()
    owner = models.CharField(max_length=24)


    class Meta:
        ordering = ('_id',)

