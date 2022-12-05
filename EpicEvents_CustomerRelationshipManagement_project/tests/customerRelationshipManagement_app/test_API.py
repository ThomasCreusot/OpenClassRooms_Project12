#import pytest

from rest_framework.test import APITestCase, APIClient

from customerRelationshipManagement_app.models import Client as AppClient  # pour ne pas confondre avec le Client Django des tests
from authentication_app.models import User


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
        content = response.content.decode()

        expected_content = '{"id":1,"firstName":"","lastName":"","email":"","phone":"","mobile":"","companyName":"test_company","dateCreated":"2022-11-28T14:55:11Z","dateUpdated":"2022-11-28T14:55:11Z","salesContact_id":1}'

        self.assertEqual(response.status_code, 201)
        self.assertTrue(AppClient.objects.exists())
        self.assertEqual(content, expected_content)

