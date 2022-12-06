#import pytest

from rest_framework.test import APITestCase, APIClient

from customerRelationshipManagement_app.models import Client as AppClient  # pour ne pas confondre avec le Client Django des tests
from customerRelationshipManagement_app.models import Contract, Event
from authentication_app.models import User


"""
Improvement could be to use the setup_method(self, method): at the begining of each Class;
However, it would be used for User creation
And with this method, User attributes are not available for tests
To be studied and improved.
"""

""" Proof of concept tests files architecture
class TestCategory(APITestCase):
    def test_b(self):
        assert 1 == 1
#>>> Works
"""

""" Proof of concept authentication
from rest_framework.test import APIClient
@pytest.mark.django_db
def test_book_infos_view():
    sales_userA = User(
        username = 'user_for_testA',
        password = 'user_for_testA',
        team = 'SALES',
    )
    sales_userA.save()

    AppClient.objects.create(
        companyName = 'test_company',
        dateCreated = '2022-11-28T14:55:11Z',
        dateUpdated = '2022-11-28T14:55:11Z',
        salesContact_id = sales_userA,
    )

    user = User.objects.get(username='user_for_testA')
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get('/api/clients/')
    content = response.content.decode()
    print(content)
#>>> Works
"""


class ClientTests(APITestCase):
    def test_client_a_sales_member_can_create(self):
        """Tests if an User from SALES team can create a Client object"""

        # Creation of a User object
        sales_user_A = User(
                username = 'user_for_testA',
                password = 'user_for_testA',
                team = 'SALES',
            )
        sales_user_A.save()

        # Django API client for sales_user_A
        client_sales_user_A = APIClient()
        client_sales_user_A.force_authenticate(user=sales_user_A)

        # Empty database
        self.assertFalse(AppClient.objects.exists())

        # Creation of a Client object in the database 
        data = {'companyName' : 'test_company',
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'salesContact_id' : sales_user_A.id,
        }

        # The User from SALES team creates a Client object
        response = client_sales_user_A.post('/api/clients/', data)

        # ID of the first object in AppClient.objects.all() queryset 
        tested_AppClient_object_id = AppClient.objects.all()[0].id

        expected_content = {'id': tested_AppClient_object_id, 
            'firstName': '', 'lastName': '', 'email': '', 'phone': '', 'mobile': '',
            'companyName': 'test_company', 'dateCreated': '2022-11-28T14:55:11Z',
            'dateUpdated': '2022-11-28T14:55:11Z',
            'salesContact_id': sales_user_A.id}

        self.assertEqual(response.status_code, 201)
        self.assertTrue(AppClient.objects.exists())
        self.assertEqual(response.json(), expected_content)

    def test_client_a_sales_member_can_read(self):
        """Tests if an User from SALES team can read a Client object
        The user needs to create a Client before reading it"""

        # Creation of a User object
        sales_user_A = User(
                username = 'user_for_testA',
                password = 'user_for_testA',
                team = 'SALES',
            )
        sales_user_A.save()

        # Django API client for sales_user_A
        client_sales_user_A = APIClient()
        client_sales_user_A.force_authenticate(user=sales_user_A)

        # Creation of a Client object in the database 
        data = {'companyName' : 'test_company',
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'salesContact_id' : sales_user_A.id,
        }

        # The User from SALES team creates a Client object
        client_sales_user_A.post('/api/clients/', data)
 
        # ID of the first object in AppClient.objects.all() queryset 
        tested_AppClient_object_id = AppClient.objects.all()[0].id

        # The User from SALES team reads the Client object
        response = client_sales_user_A.get('/api/clients/')

        expected_content = [{'id': tested_AppClient_object_id, 'firstName': '', 'lastName': '', 'email': '', 'phone': '', 'mobile': '',
            'companyName': 'test_company', 'dateCreated': '2022-11-28T14:55:11Z',
            'dateUpdated': '2022-11-28T14:55:11Z', 'salesContact_id': sales_user_A.id}]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_content)

    def test_client_a_sales_member_can_update_a_client_he_is_associated_with(self):
        """Tests if an User from SALES team can update a Client object
        The user needs to create a Client before update it"""

        # Creation of a User object
        sales_user_A = User(
                username = 'user_for_testA',
                password = 'user_for_testA',
                team = 'SALES',
            )
        sales_user_A.save()

        # Django API client for sales_user_A
        client_sales_user_A = APIClient()
        client_sales_user_A.force_authenticate(user=sales_user_A)

        # Creation of a Client object in the database 
        data = {'companyName' : 'test_company',
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'salesContact_id' : sales_user_A.id,
        }

        # The User from SALES team creates a Client object
        client_sales_user_A.post('/api/clients/', data)
 
        # ID of the first object in AppClient.objects.all() queryset 
        tested_AppClient_object_id = AppClient.objects.all()[0].id

        # The User from SALES team updates the Client object
        updated_data = {'email': 'updated_email@mail.com',
            'companyName' : 'test_company_updated',
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'salesContact_id' : sales_user_A.id,
        }

        response = client_sales_user_A.put('/api/clients/{0}/'.format(tested_AppClient_object_id), updated_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(AppClient.objects.get(email='updated_email@mail.com').companyName, "test_company_updated")

    def test_client_a_sales_member_can_not_update_a_client_he_is_not_associated_with(self):
        """Tests if an User from SALES team can not update a Client object he is not associated with
        Another user creates a Client before"""

        # Creation of two User object
        sales_user_A = User(
                username = 'user_for_testA',
                password = 'user_for_testA',
                team = 'SALES',
            )
        sales_user_A.save()

        sales_user_B = User(
                username = 'user_for_testB',
                password = 'user_for_testB',
                team = 'SALES',
            )
        sales_user_B.save()


        # Django API client for sales_user_A
        client_sales_user_A = APIClient()
        client_sales_user_A.force_authenticate(user=sales_user_A)

        # Creation of a Client object in the database 
        data = {'companyName' : 'test_company',
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'salesContact_id' : sales_user_A.id,
        }

        # The User from SALES team creates a Client object
        client_sales_user_A.post('/api/clients/', data)
 
        # ID of the first object in AppClient.objects.all() queryset 
        tested_AppClient_object_id = AppClient.objects.all()[0].id

        # Django API client for sales_user_B
        client_sales_user_B = APIClient()
        client_sales_user_B.force_authenticate(user=sales_user_B)

        # The User from SALES team updates the Client object
        updated_data = {'email': 'updated_email@mail.com',
            'companyName' : 'test_company_updated',
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'salesContact_id' : sales_user_A.id,
        }

        response = client_sales_user_B.put('/api/clients/{0}/'.format(tested_AppClient_object_id), updated_data)

        expected_content = '{"detail":"You are not allowed to do this action, see permissions.py / ClientsPermission"}'

        self.assertEqual(response.status_code, 403)
        self.assertEqual(AppClient.objects.get(email='').companyName, "test_company")
        self.assertEqual(response.content.decode(), expected_content)

    def test_client_a_sales_member_can_not_delete(self):
        """Tests if an User from SALES team can delete a Client object
        The user needs to create a Client before triyng to delete it"""

        # Creation of a User object
        sales_user_A = User(
                username = 'user_for_testA',
                password = 'user_for_testA',
                team = 'SALES',
            )
        sales_user_A.save()

        # Django API client for sales_user_A
        client_sales_user_A = APIClient()
        client_sales_user_A.force_authenticate(user=sales_user_A)

        # Creation of a Client object in the database 
        data = {'companyName' : 'test_company',
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'salesContact_id' : sales_user_A.id,
        }

        # The User from SALES team creates a Client object
        client_sales_user_A.post('/api/clients/', data)

        # ID of the first object in AppClient.objects.all() queryset 
        tested_AppClient_object_id = AppClient.objects.all()[0].id

        # The User from SALES team tries to delete the Client object
        response = client_sales_user_A.delete('/api/clients/{0}/'.format(tested_AppClient_object_id))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(AppClient.objects.exists())

    def test_client_a_support_member_can_not_create(self):
        """Tests if an User from SUPPORT team can not create a Client object"""

        # Creation of a User object
        support_user_A = User(
                username = 'user_for_testA',
                password = 'user_for_testA',
                team = 'SUPPORT',
            )
        support_user_A.save()

        # Django API client for sales_user_A
        client_support_user_A = APIClient()
        client_support_user_A.force_authenticate(user=support_user_A)

        # Empty database
        self.assertFalse(AppClient.objects.exists())

        # Creation of a Client object in the database 
        data = {'companyName' : 'test_company',
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'salesContact_id' : support_user_A.id,
        }

        # The User from SALES team creates a Client object
        response = client_support_user_A.post('/api/clients/', data)

        expected_content = {"detail":"You are not allowed to do this action, see permissions.py / ClientsPermission"}

        self.assertEqual(response.status_code, 403)
        self.assertFalse(AppClient.objects.exists())
        self.assertEqual(response.json(), expected_content)

    def test_client_a_support_member_can_read_as_he_is_the_SupportContact_of_the_client_event(self):
        """Tests if an User from SUPPORT team can read a Client object
        A Client, a Contract and an Event must be created before the support asks to read the client object"""

        # USERS
        # Creation of a User object
        sales_user_A = User(
                username = 'user_for_testA',
                password = 'user_for_testA',
                team = 'SALES',
            )
        sales_user_A.save()

        # Creation of a User object
        support_user_B = User(
                username = 'user_for_testB',
                password = 'user_for_testB',
                team = 'SUPPORT',
            )
        support_user_B.save()

        # Django API client for sales_user_A
        client_sales_user_A = APIClient()
        client_sales_user_A.force_authenticate(user=sales_user_A)

        # CLIENT OBJECT
        # Creation of a Client object in the database
        client_object_data = {'companyName' : 'test_company',
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'salesContact_id' : sales_user_A.id,
        }

        # The User from SALES team creates a Client object
        client_sales_user_A.post('/api/clients/', client_object_data)

        # ID of the first object in AppClient.objects.all() queryset 
        tested_AppClient_object_id = AppClient.objects.all()[0].id

        # CONTRACT OBJECT
        # Creation of a Contract object in the database
        contract_object_data = {'salesContact' : sales_user_A.id,
            'client' : tested_AppClient_object_id,
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'amount' : 1,
            'paymentDue' : '2022-11-28T14:55:11Z',
        }

        # The User from SALES team creates a Contract object
        client_sales_user_A.post('/api/contracts/', contract_object_data)

        # ID of the first object in Contract.objects.all() queryset 
        tested_Contract_object_id = Contract.objects.all()[0].id

        # EVENT OBJECT
        # Creation of an Event object in the database
        event_object_data = {
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',            

            'supportContact' : support_user_B.id,
            'eventStatus' : tested_Contract_object_id,
            'attendees' : 1,
            'eventDate' : '2022-11-28T14:55:11Z',
        }

        # The User from SALES team creates an event object
        client_sales_user_A.post('/api/events/', event_object_data)

        # SUPPORT USER READS EVENT OBJECT 
        # Django API client for support_user_B
        client_support_user_B = APIClient()
        client_support_user_B.force_authenticate(user=support_user_B)

        # The User from SALES team reads the Client object
        response = client_support_user_B.get('/api/clients/')

        # ID of the first object in Event.objects.all() queryset 
        #tested_Event_object_id = Event.objects.all()[0].id

        #expected_content = [{'id': tested_Event_object_id,
        #    'dateCreated': '2022-11-28T14:55:11Z',
        #    'dateUpdated': '2022-11-28T14:55:11Z',
        #    'supportContact': support_user_B.id,
        #    'eventStatus': tested_Contract_object_id,
        #    'attendees': 1,
        #    'eventDate': '2022-11-28T14:55:11Z',
        #    'notes': ''}]

        expected_content = [{'id': tested_AppClient_object_id, 'firstName': '', 'lastName': '', 'email': '', 'phone': '',
        'mobile': '', 'companyName': 'test_company', 'dateCreated': '2022-11-28T14:55:11Z',
        'dateUpdated': '2022-11-28T14:55:11Z', 'salesContact_id': sales_user_A.id}]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_content)

    def test_client_a_support_member_can_not_read_as_he_is_not_the_SupportContact_of_the_client_event(self):
        """Tests if an User from SUPPORT team can read a Client object
        A Client, a Contract and an Event must be created before the support asks to read the client object"""

        # USERS
        # Creation of a User object
        sales_user_A = User(
                username = 'user_for_testA',
                password = 'user_for_testA',
                team = 'SALES',
            )
        sales_user_A.save()

        # Creation of a User object
        support_user_B = User(
                username = 'user_for_testB',
                password = 'user_for_testB',
                team = 'SUPPORT',
            )
        support_user_B.save()

        # Creation of a User object
        support_user_C = User(
                username = 'user_for_testC',
                password = 'user_for_testC',
                team = 'SUPPORT',
            )
        support_user_C.save()

        # Django API client for sales_user_A
        client_sales_user_A = APIClient()
        client_sales_user_A.force_authenticate(user=sales_user_A)

        # CLIENT OBJECT
        # Creation of a Client object in the database
        client_object_data = {'companyName' : 'test_company',
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'salesContact_id' : sales_user_A.id,
        }

        # The User from SALES team creates a Client object
        client_sales_user_A.post('/api/clients/', client_object_data)

        # ID of the first object in AppClient.objects.all() queryset 
        tested_AppClient_object_id = AppClient.objects.all()[0].id

        # CONTRACT OBJECT
        # Creation of a Contract object in the database
        contract_object_data = {'salesContact' : sales_user_A.id,
            'client' : tested_AppClient_object_id,
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'amount' : 1,
            'paymentDue' : '2022-11-28T14:55:11Z',
        }

        # The User from SALES team creates a Contract object
        client_sales_user_A.post('/api/contracts/', contract_object_data)

        # ID of the first object in Contract.objects.all() queryset 
        tested_Contract_object_id = Contract.objects.all()[0].id

        # EVENT OBJECT
        # Creation of an Event object in the database
        event_object_data = {
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',            

            'supportContact' : support_user_B.id,
            'eventStatus' : tested_Contract_object_id,
            'attendees' : 1,
            'eventDate' : '2022-11-28T14:55:11Z',
        }

        # The User from SALES team creates an event object
        client_sales_user_A.post('/api/events/', event_object_data)

        # SUPPORT USER CAN NOT READ EVENT OBJECT 
        # Django API client for support_user_C
        client_support_user_C = APIClient()
        client_support_user_C.force_authenticate(user=support_user_C)

        # The User from SALES team reads the Client object
        response = client_support_user_C.get('/api/clients/')
        expected_content = []
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_content)

        # TEST ON DETAIL VIEW
        # ID of the first object in Contract.objects.all() queryset 
        tested_Event_object_id = Contract.objects.all()[0].id
        response = client_support_user_C.get('/api/clients/{0}/'.format(tested_Event_object_id))
        expected_content = {'detail': 'Not found.'}
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), expected_content)

    def test_client_a_support_member_can_not_update_a_client(self):
        """Tests if an User from SUPPORT team can not update a Client object
        Another user creates a Client before"""

        # Creation of two User object
        sales_user_A = User(
                username = 'user_for_testA',
                password = 'user_for_testA',
                team = 'SALES',
            )
        sales_user_A.save()

        support_user_B = User(
                username = 'user_for_testB',
                password = 'user_for_testB',
                team = 'SUPPORT',
            )
        support_user_B.save()


        # Django API client for sales_user_A
        client_sales_user_A = APIClient()
        client_sales_user_A.force_authenticate(user=sales_user_A)

        # Creation of a Client object in the database 
        data = {'companyName' : 'test_company',
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'salesContact_id' : sales_user_A.id,
        }

        # The User from SALES team creates a Client object
        client_sales_user_A.post('/api/clients/', data)
 
        # ID of the first object in AppClient.objects.all() queryset 
        tested_AppClient_object_id = AppClient.objects.all()[0].id

        # Django API client for sales_user_A
        client_support_user_B = APIClient()
        client_support_user_B.force_authenticate(user=support_user_B)

        # The User from SALES team updates the Client object
        updated_data = {'email': 'updated_email@mail.com',
            'companyName' : 'test_company_updated',
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'salesContact_id' : sales_user_A.id,
        }

        response = client_support_user_B.put('/api/clients/{0}/'.format(tested_AppClient_object_id), updated_data)

        expected_content = '{"detail":"Not found."}'

        self.assertEqual(response.status_code, 404)
        self.assertEqual(AppClient.objects.get(email='').companyName, "test_company")
        self.assertEqual(response.content.decode(), expected_content)

    def test_client_a_support_member_can_not_delete(self):
        """Tests if an User from SUPPORT team can delete a Client object
        Another user creates a Client before"""

        # Creation of two User object
        sales_user_A = User(
                username = 'user_for_testA',
                password = 'user_for_testA',
                team = 'SALES',
            )
        sales_user_A.save()

        support_user_B = User(
                username = 'user_for_testB',
                password = 'user_for_testB',
                team = 'SUPPORT',
            )
        support_user_B.save()


        # Django API client for sales_user_A
        client_sales_user_A = APIClient()
        client_sales_user_A.force_authenticate(user=sales_user_A)

        # Creation of a Client object in the database 
        data = {'companyName' : 'test_company',
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'salesContact_id' : sales_user_A.id,
        }

        # The User from SALES team creates a Client object
        client_sales_user_A.post('/api/clients/', data)
 
        # ID of the first object in AppClient.objects.all() queryset 
        tested_AppClient_object_id = AppClient.objects.all()[0].id

        # Django API client for sales_user_A
        client_support_user_B = APIClient()
        client_support_user_B.force_authenticate(user=support_user_B)

        # The User from SUPPORT team tries to delete the Client object
        response = client_support_user_B.delete('/api/clients/{0}/'.format(tested_AppClient_object_id))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(AppClient.objects.exists())


class ContractTests(APITestCase):
    def test_contract_a_sales_member_can_create(self):
        """Tests if an User from SALES team can create a Contract object"""

        # Creation of a User object
        sales_user_A = User(
                username = 'user_for_testA',
                password = 'user_for_testA',
                team = 'SALES',
            )
        sales_user_A.save()

        # Django API client for sales_user_A
        client_sales_user_A = APIClient()
        client_sales_user_A.force_authenticate(user=sales_user_A)

        # CLIENT OBJECT
        # Creation of a Client object in the database 
        data = {'companyName' : 'test_company',
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'salesContact_id' : sales_user_A.id,
        }

        # The User from SALES team creates a Client object
        client_sales_user_A.post('/api/clients/', data)

        # ID of the first object in AppClient.objects.all() queryset 
        tested_AppClient_object_id = AppClient.objects.all()[0].id

        # Empty database
        self.assertFalse(Contract.objects.exists())

        # CONTRACT OBJECT
        # Creation of a Contract object in the database
        contract_object_data = {'salesContact' : sales_user_A.id,
            'client' : tested_AppClient_object_id,
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'status': False,
            'amount' : 1,
            'paymentDue' : '2022-11-28T14:55:11Z',
        }

        # The User from SALES team creates a Contract object
        response = client_sales_user_A.post('/api/contracts/', contract_object_data)

        # ID of the first object in Contract.objects.all() queryset 
        tested_Contract_object_id = Contract.objects.all()[0].id

        expected_content = {'id' : tested_Contract_object_id,
            'salesContact' : sales_user_A.id,
            'client' : tested_AppClient_object_id,
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'status': False,
            'amount' : 1,
            'paymentDue' : '2022-11-28T14:55:11Z',
        }

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Contract.objects.exists())
        self.assertEqual(response.json(), expected_content)

    def test_contract_a_sales_member_can_read(self):
        """Tests if an User from SALES team can read a Contract object
        The user needs to create a Client and a Contract before reading it"""

        # Creation of a User object
        sales_user_A = User(
                username = 'user_for_testA',
                password = 'user_for_testA',
                team = 'SALES',
            )
        sales_user_A.save()

        # Django API client for sales_user_A
        client_sales_user_A = APIClient()
        client_sales_user_A.force_authenticate(user=sales_user_A)

        # CLIENT OBJECT
        # Creation of a Client object in the database 
        data = {'companyName' : 'test_company',
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'salesContact_id' : sales_user_A.id,
        }

        # The User from SALES team creates a Client object
        client_sales_user_A.post('/api/clients/', data)

        # ID of the first object in AppClient.objects.all() queryset 
        tested_AppClient_object_id = AppClient.objects.all()[0].id

        # Empty database
        self.assertFalse(Contract.objects.exists())

        # CONTRACT OBJECT
        # Creation of a Contract object in the database
        contract_object_data = {'salesContact' : sales_user_A.id,
            'client' : tested_AppClient_object_id,
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'status': False,
            'amount' : 1,
            'paymentDue' : '2022-11-28T14:55:11Z',
        }

        # The User from SALES team creates a Contract object
        response = client_sales_user_A.post('/api/contracts/', contract_object_data)

        # ID of the first object in Contract.objects.all() queryset 
        tested_Contract_object_id = Contract.objects.all()[0].id

        # The User from SALES team reads the Contract object
        response = client_sales_user_A.get('/api/contracts/')

        expected_content = [{'id' : tested_Contract_object_id,
            'salesContact' : sales_user_A.id,
            'client' : tested_AppClient_object_id,
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'status': False,
            'amount' : 1,
            'paymentDue' : '2022-11-28T14:55:11Z',
        }]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_content)

    def test_contract_a_sales_member_can_update_a_contract_of_a_client_he_is_associated_with(self):
        """Tests if an User from SALES team can update a Contract object of a client he is associated with
        The user needs to create a Client and a Contract before updating it"""

        # Creation of a User object
        sales_user_A = User(
                username = 'user_for_testA',
                password = 'user_for_testA',
                team = 'SALES',
            )
        sales_user_A.save()

        # Django API client for sales_user_A
        client_sales_user_A = APIClient()
        client_sales_user_A.force_authenticate(user=sales_user_A)

        # CLIENT OBJECT
        # Creation of a Client object in the database 
        data = {'companyName' : 'test_company',
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'salesContact_id' : sales_user_A.id,
        }

        # The User from SALES team creates a Client object
        client_sales_user_A.post('/api/clients/', data)

        # ID of the first object in AppClient.objects.all() queryset 
        tested_AppClient_object_id = AppClient.objects.all()[0].id

        # Empty database
        self.assertFalse(Contract.objects.exists())

        # CONTRACT OBJECT
        # Creation of a Contract object in the database
        contract_object_data = {'salesContact' : sales_user_A.id,
            'client' : tested_AppClient_object_id,
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'status': False,
            'amount' : 1,
            'paymentDue' : '2022-11-28T14:55:11Z',
        }

        # The User from SALES team creates a Contract object
        response = client_sales_user_A.post('/api/contracts/', contract_object_data)

        # ID of the first object in Contract.objects.all() queryset 
        tested_Contract_object_id = Contract.objects.all()[0].id

        # The User from SALES team updates the Contract  object
        updated_data = {'salesContact' : sales_user_A.id,
            'client' : tested_AppClient_object_id,
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'status': True,
            'amount' : 10,
            'paymentDue' : '2022-11-28T14:55:11Z',
        }

        response = client_sales_user_A.put('/api/contracts/{0}/'.format(tested_Contract_object_id), updated_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contract.objects.get(dateCreated='2022-11-28T14:55:11Z').status, True)

    def test_contract_a_sales_member_can_not_update_a_contract_of_a_client_he_is_not_associated_with(self):
        """Tests if an User from SALES team can update a Contract object of a client he is not associated with
        Another user needs to create a Client and a Contract before updating it"""

        # Creation of a User object
        sales_user_A = User(
                username = 'user_for_testA',
                password = 'user_for_testA',
                team = 'SALES',
            )
        sales_user_A.save()

        sales_user_B = User(
                username = 'user_for_testB',
                password = 'user_for_testB',
                team = 'SALES',
            )
        sales_user_B.save()

        # Django API client for sales_user_A
        client_sales_user_A = APIClient()
        client_sales_user_A.force_authenticate(user=sales_user_A)

        # CLIENT OBJECT
        # Creation of a Client object in the database 
        data = {'companyName' : 'test_company',
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'salesContact_id' : sales_user_A.id,
        }

        # The User from SALES team creates a Client object
        client_sales_user_A.post('/api/clients/', data)

        # ID of the first object in AppClient.objects.all() queryset 
        tested_AppClient_object_id = AppClient.objects.all()[0].id

        # Empty database
        self.assertFalse(Contract.objects.exists())

        # CONTRACT OBJECT
        # Creation of a Contract object in the database
        contract_object_data = {'salesContact' : sales_user_A.id,
            'client' : tested_AppClient_object_id,
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'status': False,
            'amount' : 1,
            'paymentDue' : '2022-11-28T14:55:11Z',
        }

        # The User from SALES team creates a Contract object
        response = client_sales_user_A.post('/api/contracts/', contract_object_data)

        # ID of the first object in Contract.objects.all() queryset 
        tested_Contract_object_id = Contract.objects.all()[0].id

        # Django API client for sales_user_B
        client_sales_user_B = APIClient()
        client_sales_user_B.force_authenticate(user=sales_user_B)

        # The User from SALES team updates the Contract  object
        updated_data = {'salesContact' : sales_user_A.id,
            'client' : tested_AppClient_object_id,
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'status': True,
            'amount' : 10,
            'paymentDue' : '2022-11-28T14:55:11Z',
        }

        response = client_sales_user_B.put('/api/contracts/{0}/'.format(tested_Contract_object_id), updated_data)

        expected_content = '{"detail":"You are not allowed to do this action, see permissions.py / ContractsPermission"}'

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Contract.objects.get(dateCreated='2022-11-28T14:55:11Z').status, False)
        self.assertEqual(response.content.decode(), expected_content)

    def test_contract_a_sales_member_can_not_delete(self):
        """Tests if an User from SALES team can delete a Client object
        The user needs to create a Client before triyng to delete it"""

        # Creation of a User object
        sales_user_A = User(
                username = 'user_for_testA',
                password = 'user_for_testA',
                team = 'SALES',
            )
        sales_user_A.save()

        # Django API client for sales_user_A
        client_sales_user_A = APIClient()
        client_sales_user_A.force_authenticate(user=sales_user_A)

        # CLIENT OBJECT
        # Creation of a Client object in the database 
        data = {'companyName' : 'test_company',
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'salesContact_id' : sales_user_A.id,
        }

        # The User from SALES team creates a Client object
        client_sales_user_A.post('/api/clients/', data)

        # ID of the first object in AppClient.objects.all() queryset 
        tested_AppClient_object_id = AppClient.objects.all()[0].id

        # Empty database
        self.assertFalse(Contract.objects.exists())

        # CONTRACT OBJECT
        # Creation of a Contract object in the database
        contract_object_data = {'salesContact' : sales_user_A.id,
            'client' : tested_AppClient_object_id,
            'dateCreated' : '2022-11-28T14:55:11Z',
            'dateUpdated' : '2022-11-28T14:55:11Z',
            'status': False,
            'amount' : 1,
            'paymentDue' : '2022-11-28T14:55:11Z',
        }

        # The User from SALES team creates a Contract object
        response = client_sales_user_A.post('/api/contracts/', contract_object_data)

        # ID of the first object in Contract.objects.all() queryset 
        tested_Contract_object_id = Contract.objects.all()[0].id

        # The User from SALES team tries to delete the Client object
        response = client_sales_user_A.delete('/api/contracts/{0}/'.format(tested_Contract_object_id))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(AppClient.objects.exists())