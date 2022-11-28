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

- For more details, please refer to the [endpoints documentation](https://documenter.getpostman.com/view/ TO BE DONE).


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
The example chosen is a user who make a GET request on http://127.0.0.1:8000/api/...... to get ..... . 

## Example of request and response 

### Request
```
curl --location --request GET 'http://127.0.0.1:8000/api/projects/30/issues/' \
--header 'Authorization: Bearer TOKEN' \
```

### API response
All issues related to the project 30
```json
[
    TBD
]
```

## Corresponding code

### urls.py
```python
projects_issues_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
projects_issues_router.register('issues', IssueViewset, basename='project-issues')
```

### views.py
```python
class TBD:

```

### serializers.py
```python
class TBD(ModelSerializer):

```

### permissions.py
```python
TBD
```
