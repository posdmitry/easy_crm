from django.test import TestCase
from rest_framework.test import APIClient

from clients.models import Industries
from clients_api.serializers import ClientsSerializer


class ClientSerializerTestCase(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_client(self):
        contact_persons = [
            {
                "name": "Volodymir",
                "role": "SEO",
                "phone_number": "0674635955",
                "email": "",
                "telegram": ""
            },
            {
                "name": "Sasha",
                "role": "sales",
                "phone_number": "0670000000",
                "email": "",
                "telegram": ""
            },
        ]

        data = {
            "name": "Test",
            "type": "Client",
            "industries": [
                {"name": "Foam"}
            ],
            "contact_persons": contact_persons,
        }


        # response = self.client.post('', data=data, format='json')
        # assert response.status_code == 200
        # request = self.factory.post('api/', data=data, format='json')
        # get_c = self.factory.get('api')
        industry = Industries.objects.create(name="Foam")
        industry.save()
        serializer = ClientsSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        self.assertTrue(serializer.is_valid())

    def test_create_client_empty_indusrties(self):
        contact_persons = [
            {
                "name": "Volodymir",
                "role": "SEO",
                "phone_number": "0674635955",
                "email": "",
                "telegram": ""
            },
            {
                "name": "Sasha",
                "role": "sales",
                "phone_number": "0670000000",
                "email": "",
                "telegram": ""
            },
        ]

        data = {
            "name": "Test",
            "contact_persons": contact_persons,
        }

        serializer = ClientsSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        self.assertTrue(serializer.is_valid())

    # def test_get_messages(self):
    #     response = self.client.get('/messages/', format='json')
    #     assert response.status_code == 200
