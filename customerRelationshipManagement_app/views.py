from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from customerRelationshipManagement_app.models import Client
from customerRelationshipManagement_app.serializers import ClientSerializer


def index(request):
    obj = Client.objects.all()
    context={
        "obj": obj,
    }
    return render(request, 'index.html', context=context)


class ClientViewset(ModelViewSet):
    """API endpoint that allows Clients to be CRUD."""

    serializer_class = ClientSerializer

    def get_queryset(self):
        # return Client.objects.filter(=self.kwargs[''])
        return Client.objects.all()
