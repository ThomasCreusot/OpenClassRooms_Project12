# OpenClassRooms_Project12
Develop a secure back-end architecture using Django ORM


# Project presentation
The present project is the twelfth one of the training course *Python Application Developer*, offered by OpenClassRooms and aims to *Develop a secure back-end architecture using Django ORM*.

The main goal is to develop a **Customer relationship management** wich allows users to **manage clients, contracts and events**. 
Users are from the following teams/departments: Manager, Sales, Support

According to the specifications, this API must:
- use Django REST and PostgreSQL
- have a front-end application with Django administration website for Managers users
- allow users to: CRUD Clients, CRUD Contracts for a client, CRUD Events related to a contract, depending on their team/department
- allow user to filter/search data (within the URL) :
    - search a Client object with its lastName or email
        - e.g. : http://127.0.0.1:8000/api/clients/?lastName=FirstClient__Lname&email=FirstClient_@mail.com
    - search a Contract with its creationDate or its amount; or with the lastName or email of the Client related to the Contract
    - search an Event with its eventDate or the lastName or email of the Client related to the Event

- For more details, please refer to the [endpoints documentation](https://documenter.getpostman.com/view/20371598/2s8YsxuWzk).


# Project execution
To correctly execute the program, you need to activate the associated virtual environment which has been recorded in the ‘requirements.txt’ file.

## To create and activate the virtual environment 
Please follow theses instructions:

1. Open your Shell 
-Windows: 
>'windows + R' 
>'cmd'  
-Mac: 
>'Applications > Utilitaires > Terminal.app'

2. Find the folder which contains the program (with *cd* command)

3. Create a virtual environment: write the following command in the console
>'python -m venv env'

4. Activate this virtual environment: 
-Linux or Mac: write the following command in the console
>'source env/bin/activate'
-Windows: write the following command in the console 
>'env\Scripts\activate'

5. Install the python packages recorded in the *requirements.txt* file: write in the console the following command
>'pip install -r requirements.txt'

## To get a superuser account
6. Execute the code: write the following command in the console (Python must be installed on your computer and virtual environment must be activated)
>'python manage.py createsuperuser'
Follow the instruction

## To launch the server
Please follow this instruction
7. Execute the code: write the following command in the console (Python must be installed on your computer and virtual environment must be activated)
>'python manage.py runserver'

## To access to the API django administration website
8. Open a web browser and go on http://127.0.0.1:8000/admin/ .
You are now allowed to create User objects (Managers, Sales members or Support members), and Client, Contract and Event objects.

## To access to the API
9. Once your account is created, you can make a POST request on http://127.0.0.1:8000/api/token/ to get an access Token.
Please, write the following fields in the request body: username, password with the correspoding value

10. Then, write the following field in the request header: Authorization, with the value "Bearer TOKEN" (replace "TOKEN" by the value of your current access token, that you get at the previous step).

11. Please enjoy the API ; you can, for example make a GET request on http://127.0.0.1:8000/api/clients/ to see all clients (manager or sales member) or clients you are in charge of at least a contract (support member).


# Example of request, response and corresponding code
The example chosen is a user who make a GET request on http://127.0.0.1:8000/api/clients/ to get all clients (manager team) . 

## Example of request and response 

### Request
```
curl --location --request GET 'http://127.0.0.1:8000/api/clients/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY5NjU0MjkyLCJpYXQiOjE2Njk2NDcwOTIsImp0aSI6IjYxN2MzMjI3NzQyODQ5OWNiNzczZmIwMjZkNDZjZTYwIiwidXNlcl9pZCI6MTJ9.IT4WyQU0jhlNksJhlPaLA9PMm7hfEj_cc9sFMu1MHbs'
```

### API response
All issues related to the project 30
```json
[
    {
        "id": 8,
        "firstName": "",
        "lastName": "",
        "email": "",
        "phone": "",
        "mobile": "",
        "companyName": "The_Company_A",
        "dateCreated": "2022-11-28T14:55:11Z",
        "dateUpdated": "2022-11-28T14:55:11Z",
        "salesContact_id": 11
    }
]
```

## Corresponding code

### urls.py
```python
router = routers.SimpleRouter()
router.register('clients', ClientViewset, basename='clients') 
```

### views.py
```python
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
```

### serializers.py
```python
class ClientSerializer(ModelSerializer):
    """Serializes Client objects"""

    class Meta:
        model = Client
        fields = ['id', 'firstName', 'lastName', 'email', 'phone', 'mobile', 'companyName', 'dateCreated', 'dateUpdated', 'salesContact_id']
```

### permissions.py
```python
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
```
