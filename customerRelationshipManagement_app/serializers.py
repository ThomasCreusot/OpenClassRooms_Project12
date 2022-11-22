from rest_framework.serializers import ModelSerializer

from customerRelationshipManagement_app.models import Client

class ClientSerializer(ModelSerializer):
    """Serializes Client objects"""

    class Meta:
        model = Client
        fields = ['id', 'firstName', 'lastName', 'email', 'phone', 'mobile', 'companyName', 'dateCreated', 'dateUpdated', 'salesContact_id']
