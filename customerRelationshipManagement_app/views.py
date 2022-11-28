from django.db.models import Q
from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from customerRelationshipManagement_app.models import Client, Contract, Event
from customerRelationshipManagement_app.serializers import ClientSerializer, ContractSerializer, EventSerializer
from customerRelationshipManagement_app.permissions import ClientsPermission, ContractsPermission, EventsPermission


class ClientViewset(ModelViewSet):
    """API endpoint that allows Clients to be CRUD."""

    serializer_class = ClientSerializer

    permission_classes = [ClientsPermission]

    def get_queryset(self):
        # return Client.objects.filter(=self.kwargs[''])
        # return Client.objects.all()

        authenticatedUserTeam = self.request.user.team

        clientQueryset = Client.objects.all() 
        clientLastName = self.request.GET.get('lastName') 
        clientEmail = self.request.GET.get('email') 

        if clientLastName is not None:
            clientQueryset = clientQueryset.filter(lastName=clientLastName)
        if clientEmail is not None:
            clientQueryset = clientQueryset.filter(email=clientEmail)

        if authenticatedUserTeam == "SALES" or authenticatedUserTeam == "MANAGEMENT":
            # Sales team : READ : all clients
            return clientQueryset
        if authenticatedUserTeam == "SUPPORT":
               # Support team : READ : only clients associated to an event they manage.
            eventManagedByAuthenticatedSupportUser = Event.objects.filter(supportContact=self.request.user) 
            contractOfEventManagedByAuthenticatedSupportUser = Contract.objects.filter(contract_event__in=eventManagedByAuthenticatedSupportUser)
            # filter based on previous queryset : clientQueryset; to take account of URL research
            clientOfContractOfEventManagedByAuthenticatedSupportUser = clientQueryset.filter(client_contract__in=contractOfEventManagedByAuthenticatedSupportUser)
            return clientOfContractOfEventManagedByAuthenticatedSupportUser
        #before "if authenticatedUserTeam" code was : return clientQueryset


class ContractViewset(ModelViewSet):
    """API endpoint that allows Contracts to be CRUD."""

    serializer_class = ContractSerializer

    permission_classes = [ContractsPermission]

    def get_queryset(self):
        contractQueryset = Contract.objects.all()
        
        contractClientLastName = self.request.GET.get('lastName') 
        contractClientEmail = self.request.GET.get('email') 
        contractCreationDate = self.request.GET.get('creationDate') 
        contractAmount = self.request.GET.get('amount') 

        if contractClientLastName is not None or contractClientEmail is not None:
            if contractClientLastName is not None:
                clientQueryset = Client.objects.filter(lastName=contractClientLastName)
            if contractClientEmail is not None:
                clientQueryset = Client.objects.filter(email=contractClientEmail)
            contractQueryset = contractQueryset.filter(Q(client__in=clientQueryset))

        if contractCreationDate is not None:
            contractQueryset = contractQueryset.filter(dateCreated=contractCreationDate)

        if contractAmount is not None:
            contractQueryset = contractQueryset.filter(amount=contractAmount)

        return contractQueryset


class EventViewset(ModelViewSet):
    """API endpoint that allows Events to be CRUD."""

    serializer_class = EventSerializer

    permission_classes = [EventsPermission]

    def get_queryset(self):
        eventQueryset = Event.objects.all()
        
        eventClientLastName = self.request.GET.get('lastName') 
        eventClientEmail = self.request.GET.get('email') 
        eventDate = self.request.GET.get('eventDate') 

        if eventClientLastName is not None or eventClientEmail is not None:
            if eventClientLastName is not None :
                clientQueryset = Client.objects.filter(lastName=eventClientLastName)
            if eventClientEmail is not None:
                clientQueryset = Client.objects.filter(email=eventClientEmail)
            contractQueryset = Contract.objects.filter(Q(client__in=clientQueryset))
            eventQueryset = eventQueryset.filter(Q(eventStatus__in=contractQueryset))

        if eventDate is not None:
            eventQueryset = eventQueryset.filter(eventDate=eventDate)

        return eventQueryset