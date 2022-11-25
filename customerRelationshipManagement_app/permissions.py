# from django.shortcuts import get_object_or_404
# from django.db.models import Q

from rest_framework import permissions
from rest_framework.permissions import BasePermission

from customerRelationshipManagement_app.models import Client, Contract, Event


class ClientsPermission(BasePermission):
    """Gives permission :
    -ask to view all Client objects      : GET in has_permission  : any authentificated user can ask to view the Client objects
    -ask to create all Client objects    : POST in has_permission : only user with field 'team' = 'SALES' or 'MANAGEMENT' can ask to create a Client object
    -ask to update all Client objects    : PUT on http://127.0.0.1:8000/api/clients/ : does not exist;
    but same code as in has_object_permission (explanotion at https://www.django-rest-framework.org/api-guide/permissions/)
    -ask to delete all Client objects    : DELETE on http://127.0.0.1:8000/api/clients/ : does not exist
    but same code as in has_object_permission (explanotion at https://www.django-rest-framework.org/api-guide/permissions/)

    -ask to view a given Client object   : GET in has_object_permission :
        --users with field 'team' = 'SALES' or 'MANAGEMENT' users can see all Client objects;
        --users with field 'team' = 'SUPPORT' users can only see a Client object if they are the 'Support contact' of the Client Event; 

    -ask to create a given Client object : "Method \"POST\" not allowed." on http://127.0.0.1:8000/api/clients/1

    -ask to update a given Client object : PUT in has_object_permission : 
        --'MANAGEMENT' users: allowed to update any Client object
        --'SALES' users: allowed to update a Client if they are the Client 'Sales Contact'
        --'SUPPORT' users: not allowed to update a Client object

    -ask to delete a given Client object: not allowed yet, according to technical specifications
    """

    message = 'You are not allowed to do this action, see permissions.py / ClientsPermission'


    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user.is_authenticated)
        elif request.method == "POST":
            return bool((request.user.team == 'SALES' or request.user.team == 'MANAGEMENT') and request.user.is_authenticated)
        elif request.method == "PUT":
            #Can not copy paste code from has_object_permission as it implies 'obj'; and return True is needed for well beahviour of has_object_permission
            return True
        elif request.method == "DELETE":
            return False 

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if (request.user.team == 'SALES' or request.user.team == 'MANAGEMENT') and request.user.is_authenticated:
                return True
            elif request.user.team == 'SUPPORT' and request.user.is_authenticated:
                eventManagedByAuthenticatedSupportUser = Event.objects.filter(supportContact=request.user) 
                contractOfEventManagedByAuthenticatedSupportUser = Contract.objects.filter(contract_event__in=eventManagedByAuthenticatedSupportUser)
                clientOfContractOfEventManagedByAuthenticatedSupportUser = Client.objects.filter(client_contract__in=contractOfEventManagedByAuthenticatedSupportUser)

                permission = False
                for client in clientOfContractOfEventManagedByAuthenticatedSupportUser:
                    if obj.id == client.id:
                        permission = True
                return permission

        elif request.method == "POST":
            return False  # "Method \"POST\" not allowed."

        elif request.method == "PUT":
            if request.user.team == 'MANAGEMENT' and request.user.is_authenticated:
                return True
            elif request.user.team == 'SALES' and request.user.is_authenticated:
                return obj.salesContact_id == request.user
            elif request.user.team == 'SUPPORT' and request.user.is_authenticated:
                return False

        elif request.method == "DELETE":
            # Not allowed yet according to technical specifications
            return False

