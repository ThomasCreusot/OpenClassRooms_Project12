from rest_framework.serializers import ModelSerializer

from customerRelationshipManagement_app.models import Client, Contract, Event

class ClientSerializer(ModelSerializer):
    """Serializes Client objects"""

    class Meta:
        model = Client
        fields = ['id', 'firstName', 'lastName', 'email', 'phone', 'mobile', 'companyName', 'dateCreated', 'dateUpdated', 'salesContact_id']


class ContractSerializer(ModelSerializer):
    """Serializes Contract objects"""

    class Meta:
        model = Contract
        fields = ['id', 'salesContact', 'client', 'dateCreated', 'dateUpdated', 'status', 'amount', 'paymentDue']


class EventSerializer(ModelSerializer):
    """Serializes Event objects"""

    class Meta:
        model = Event
        fields = ['id', 'dateCreated', 'dateUpdated', 'supportContact', 'eventStatus', 'attendees', 'eventDate', 'notes']
