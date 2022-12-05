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

    response = client.get('/api/clients/')  # GET
    content = response.content.decode()
    print(content)
#>>> Works
"""


class ClientTests(APITestCase):
    def test_client_read(self):
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

        response = client.get('/api/clients/')  # GET
        content = response.content.decode()

        #response = self.client.get('/users/4/')
        #self.assertEqual(response.data, {'id': 4, 'username': 'lauren'})
