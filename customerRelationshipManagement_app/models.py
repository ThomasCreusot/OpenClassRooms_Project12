from django.db import models
from django.conf import settings

class Client(models.Model):
    """Represent a client"""

    # id: https://docs.djangoproject.com/en/4.1/topics/db/models/#automatic-primary-key-fields
    firstName = models.fields.CharField(max_length=25, blank=True)
    lastName = models.fields.CharField(max_length=25, blank=True)
    email = models.fields.CharField(max_length=100, blank=True)
    phone = models.fields.CharField(max_length=20, blank=True)
    mobile = models.fields.CharField(max_length=20, blank=True)
    companyName = models.fields.CharField(max_length=250, blank=False)
    dateCreated = models.fields.DateTimeField()
    dateUpdated = models.fields.DateTimeField()
    salesContact_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='salesTeam_client')


class Contract(models.Model):
    """Represent a contract"""

    # id: https://docs.djangoproject.com/en/4.1/topics/db/models/#automatic-primary-key-fields
    salesContact = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='salesTeam_contract')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_contract', blank=False)  # no contract without an associed client
    dateCreated = models.fields.DateTimeField()
    dateUpdated = models.fields.DateTimeField()
    status = models.fields.BooleanField()
    amount = models.fields.FloatField()
    paymentDue = models.fields.DateTimeField()


class Event(models.Model):
    """Represent an event"""

    # id: https://docs.djangoproject.com/en/4.1/topics/db/models/#automatic-primary-key-fields
    # client = INT --> information redundancy with event -> contract and contract -> client 
    dateCreated = models.fields.DateTimeField()
    dateUpdated = models.fields.DateTimeField()
    supportContact = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='supportTeam_event')

    # https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.Field.null
    # Note that when unique is True, you don’t need to specify db_index, because unique implies the creation of an index.
    # A one-to-one relationship. Conceptually, this is similar to a ForeignKey with unique=True, but the “reverse” side of the relation will directly return a single object.
    # This is most useful as the primary key of a model which “extends” another model in some way; Multi-table inheritance is implemented by adding an implicit one-to-one relation from the child model to the parent model, for example.
    # eventStatus = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='contract_event', unique=True)  # unique : relation 1-1
    eventStatus = models.OneToOneField(Contract, on_delete=models.CASCADE, related_name='contract_event')
    attendees = models.fields.IntegerField()
    eventDate = models.fields.DateTimeField()
    notes = models.fields.TextField(max_length=2048, blank=True)
