from clients_api.tests.factories import (
    ClientsFactory,
    CustomUserFactory,
    IndustriesFactory,
    ClientTypeFactory,
    ContactPersonFactory
)
from clients_api.tests.mixins import AuthenticatedTestClientMixin
from rest_framework.test import APITransactionTestCase

from clients_auth.models import CustomUser, Company


class ViewsBaseTestCase(AuthenticatedTestClientMixin, APITransactionTestCase):
    API_VERSION = "v1"
    LIST_CLIENTS = ""
    RETRIEVE_CLIENT = ""
    CREATE_CLIENT = ""
    LIST_MESSAGES = ""
    CREATE_MESSAGE = ""

    USER_IS_ADMIN = False
    USER_IS_EMPLOYEE = False

    def setUp(self, *args, **kwargs):
        self.company, _ = Company.objects.get_or_create(name='TestCompany')
        super().setUp()

    def get_test_user(self, *args, **kwargs):
        username = kwargs.get('username', 'testUser')
        company = kwargs.get('company', self.company)
        is_admin = kwargs.get('is_admin', False)
        is_employee = kwargs.get('is_employee', False)
        is_superuser = kwargs.get('is_superuser', False)
        user, _ = CustomUser.objects.get_or_create(
            username=username,
            is_superuser=is_superuser,
            company=company,
            is_admin=is_admin,
            is_employee=is_employee
        )
        return user

    def buid_client(self, user):
        user = user or CustomUserFactory()
        industries =IndustriesFactory.create_batch(3)
        cl_type = ClientTypeFactory(client_type='client')

        client = ClientsFactory(
            industries=industries,
            client_type=cl_type,
            user=user
        )

        ContactPersonFactory(role='SEO', client=client)
        ContactPersonFactory(role='manager', client=client)

        return client

    def get_list_clients_request(self):
        read_response = self.client.get(
            self.LIST_CLIENTS,
            format='json',
        )
        return read_response

    def get_retrieve_client_request(self, client_id):
        url = f"{self.RETRIEVE_CLIENT}{client_id}/"
        read_response = self.client.get(
            url,
            format='json',
        )
        return read_response

    def assert_successful_response(self, response):
        self.assertEqual(200, response.status_code)

    def assert_not_found_obj_response(self, response):
        self.assertEqual(404, response.status_code)
        self.assertEqual('Not found.', response.data.get('detail'))

    def assert_successful_get_clients_count(self, response, expected_clients: []):
        self.assertEqual(len(expected_clients), len(response.data))

    def assert_response_unknown_user(self, response):
        self.assertEqual(403, response.status_code)
        self.assertEqual("You do not have permission for this action!", response.data.get("detail"))

    def assert_client_payload(self, actual_client, expected_client):
        self.assertEqual(expected_client.id, actual_client.get("id"))
        self.assertEqual(expected_client.name, actual_client.get("name"))
        self.assertEqual(expected_client.client_type.client_type,
                         actual_client.get("client_type").get("client_type"))
        self.assertEqual(len(expected_client.industries.all()), len(actual_client.get("industries")))
        self.assertEqual(len(expected_client.contact_persons.all()), len(actual_client.get('contact_persons')))
        self.assertEqual(expected_client.user.id, actual_client.get("user"))
