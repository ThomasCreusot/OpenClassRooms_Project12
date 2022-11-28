from rest_framework import permissions
from rest_framework.permissions import BasePermission

from customerRelationshipManagement_app.models import Client, Contract, Event


def user_is_authentificated_sales_or_management(request):
    """Returns true if user is from team SALES or MANAGEMENT and is authenticated"""

    return bool((request.user.team == 'SALES' or request.user.team == 'MANAGEMENT') and request.user.is_authenticated)


def support_in_charge_of_event_related_to_client(request, obj):
    """Returns True if the authenticated user is in charge of at least an Event related to the obj of the request wich is a Client"""

    event_managed_by_authenticated_support_user = Event.objects.filter(supportContact = request.user) 
    contract_of_event_managed_by_authenticated_support_user = Contract.objects.filter(contract_event__in = event_managed_by_authenticated_support_user)
    clients_of_contract_of_event_managed_by_authenticated_support_user = Client.objects.filter(client_contract__in = contract_of_event_managed_by_authenticated_support_user)

    permission = False
    for client in clients_of_contract_of_event_managed_by_authenticated_support_user:
        if obj.id == client.id:
            permission = True
    return permission


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
            return user_is_authentificated_sales_or_management(request)
        elif request.method == "PUT":
            # Can not copy paste code from has_object_permission as it implies 'obj'; and so return
            # True is needed for well beahviour of has_object_permission
            return True
        elif request.method == "DELETE":
            return False 

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if user_is_authentificated_sales_or_management(request):
                return True
            elif request.user.team == 'SUPPORT' and request.user.is_authenticated:
                return support_in_charge_of_event_related_to_client(request, obj)

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


class ContractsPermission(BasePermission):
    """Gives permission :
    -ask to view all Contract objects      : GET in has_permission  : any authentificated user can ask to view the Contract objects
    -ask to create all Contract objects    : POST in has_permission : only user with field 'team' = 'SALES' or 'MANAGEMENT' can ask to create a Contract object

    -ask to update all Contract objects    : PUT on http://127.0.0.1:8000/api/contracts/ : does not exist;
    but same code as in has_object_permission (explanotion at https://www.django-rest-framework.org/api-guide/permissions/)
    -ask to delete all Contract objects    : DELETE on http://127.0.0.1:8000/api/contracts/ : does not exist
    but same code as in has_object_permission (explanotion at https://www.django-rest-framework.org/api-guide/permissions/)

    -ask to view a given Contract object   : GET in has_object_permission : any authentificated user can ask to view the Contract objects

    -ask to create a given Contract object : "Method \"POST\" not allowed." on http://127.0.0.1:8000/api/contract/1

    -ask to update a given Contract object : PUT in has_object_permission : 
        --'MANAGEMENT' users: allowed to update any Contract object
        --'SALES' users: allowed to update a Contract if they are the 'Sales Contact' of Client related to the contract
        --'SUPPORT' users: not allowed to update a Contract object

    -ask to delete a given Contract object: not allowed yet, according to technical specifications
    """

    message = 'You are not allowed to do this action, see permissions.py / ContractsPermission'


    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user.is_authenticated)
        elif request.method == "POST":
            return user_is_authentificated_sales_or_management(request)
        elif request.method == "PUT":
            # Can not copy paste code from has_object_permission as it implies 'obj'; and so return
            # True is needed for well beahviour of has_object_permission
            return True
        elif request.method == "DELETE":
            return False 

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user.is_authenticated)

        elif request.method == "POST":
            return False  # "Method \"POST\" not allowed."

        elif request.method == "PUT":
            if request.user.team == 'MANAGEMENT' and request.user.is_authenticated:
                return True
            elif request.user.team == 'SALES' and request.user.is_authenticated:
                return obj.client.salesContact_id == request.user
            elif request.user.team == 'SUPPORT' and request.user.is_authenticated:
                return False

        elif request.method == "DELETE":
            # Not allowed yet according to technical specifications
            return False


class EventsPermission(BasePermission):
    """Gives permission :
    -ask to view all Event objects      : GET in has_permission  : any authentificated user can ask to view the Event objects
    -ask to create all Event objects    : POST in has_permission : only user with field 'team' = 'SALES' or 'MANAGEMENT' can ask to create a Event object

    -ask to update all Event objects    : PUT on http://127.0.0.1:8000/api/events/ : does not exist;
    but same code as in has_object_permission (explanotion at https://www.django-rest-framework.org/api-guide/permissions/)
    -ask to delete all Event objects    : DELETE on http://127.0.0.1:8000/api/events/ : does not exist
    but same code as in has_object_permission (explanotion at https://www.django-rest-framework.org/api-guide/permissions/)

    -ask to view a given Event object   : GET in has_object_permission : any authentificated user can ask to view the Event objects

    -ask to create a given Event object : "Method \"POST\" not allowed." on http://127.0.0.1:8000/api/event/1

    -ask to update a given Event object : PUT in has_object_permission : 
        --'MANAGEMENT' users: allowed to update any Event object
        --'SALES' users: allowed to update an Event if they are the 'Sales Contact' of Client related to the contract of the event
        --'SUPPORT' users: allowed to update an Event if they are the Event 'supportContact'

    -ask to delete a given Event object: not allowed yet, according to technical specifications
    """

    message = 'You are not allowed to do this action, see permissions.py / EventsPermission'


    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user.is_authenticated)
        elif request.method == "POST":
            return user_is_authentificated_sales_or_management(request)
        elif request.method == "PUT":
            # Can not copy paste code from has_object_permission as it implies 'obj'; and so return
            # True is needed for well beahviour of has_object_permission
            return True
        elif request.method == "DELETE":
            return False 

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user.is_authenticated)

        elif request.method == "POST":
            return False  # "Method \"POST\" not allowed."

        elif request.method == "PUT":
            if request.user.team == 'MANAGEMENT' and request.user.is_authenticated:
                return True
            elif request.user.team == 'SALES' and request.user.is_authenticated:
                return obj.eventStatus.client.salesContact_id == request.user
            elif request.user.team == 'SUPPORT' and request.user.is_authenticated:
                return obj.supportContact == request.user

        elif request.method == "DELETE":
            # Not allowed yet according to technical specifications
            return False
