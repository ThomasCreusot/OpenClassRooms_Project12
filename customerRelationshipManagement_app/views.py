from django.db.models import Q
from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from customerRelationshipManagement_app.models import Client, Contract, Event
from customerRelationshipManagement_app.serializers import ClientSerializer, ContractSerializer, EventSerializer


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
        # return Client.objects.all()
        clientQueryset = Client.objects.all() 
        clientLastName = self.request.GET.get('lastName') 
        clientEmail = self.request.GET.get('email') 
        if clientLastName is not None:
            clientQueryset = clientQueryset.filter(lastName=clientLastName)
        if clientEmail is not None:
            clientQueryset = clientQueryset.filter(email=clientEmail)
        return clientQueryset


class ContractViewset(ModelViewSet):
    """API endpoint that allows Contracts to be CRUD."""

    serializer_class = ContractSerializer

    def get_queryset(self):
        contractQueryset = Contract.objects.all()
        
        contractClientLastName = self.request.GET.get('lastName') 
        contractClientEmail = self.request.GET.get('email') 
        contractCreationDate = self.request.GET.get('creationDate') 
        contractAmount = self.request.GET.get('amount') 

        if contractClientLastName is not None:
            clientQueryset = Client.objects.filter(lastName=contractClientLastName)
            contractQueryset = contractQueryset.filter(
                Q(client__in=clientQueryset)
            )

        if contractClientEmail is not None:
            clientQueryset = Client.objects.filter(email=contractClientEmail)
            contractQueryset = contractQueryset.filter(
                Q(client__in=clientQueryset)
            )

        if contractCreationDate is not None:
            contractQueryset = contractQueryset.filter(dateCreated=contractCreationDate)

        return contractQueryset


class EventViewset(ModelViewSet):
    """API endpoint that allows Events to be CRUD."""

    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.all()
