from json import dumps

from clients_api.tests.factories import (
    ClientsFactory,
    CustomUserFactory,
    IndustriesFactory,
    ClientTypeFactory,
    ContactPersonFactory, MessagesFactory
)
from clients_api.tests.mixins import AuthenticatedTestClientMixin
from rest_framework.test import APITransactionTestCase

from clients_auth.models import CustomUser, Company


class ViewsBaseTestCase(AuthenticatedTestClientMixin, APITransactionTestCase):
    API_VERSION = "v1"
    LIST_CLIENTS = ""
    RETRIEVE_CLIENT = ""
    CREATE_CLIENT = ""
    UPDATE_CLIENT = ""
    DELETE_CLIENT = ""
    CREATE_MESSAGE = ""
    LIST_CLIENT_TYPES = ""
    LIST_INDUSTRIES = ""

    def setUp(self, *args, **kwargs):
        self.company, _ = Company.objects.get_or_create(name='TestCompany')
        self.strange_company, _ = Company.objects.get_or_create(name='Strange Company')
        self.admin_user = {'username': 'testUser1', 'company': self.company, 'is_admin': True}
        self.employee_user = {'username': 'testUser2', 'company': self.company, 'is_employee': True}
        self.strange_employee_user = {'username': 'testUser3', 'company': self.strange_company, 'is_employee': True}
        self.superuser = {'username': 'testUser3', 'is_superuser': True}
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

    def build_client(self, user):
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

        MessagesFactory.create_batch(3, client=client)

        return client

    def build_client_types(self):
        client_type = ClientTypeFactory.create_batch(4)
        return client_type

    def build_industries(self):
        industries = IndustriesFactory.create_batch(5)
        return industries

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

    def get_list_client_types_request(self):
        read_response = self.client.get(
            self.LIST_CLIENT_TYPES,
            format='json',
        )
        return read_response

    def get_list_industries(self):
        read_response = self.client.get(
            self.LIST_INDUSTRIES,
            format='json',
        )
        return read_response

    def post_create_client(self, payload):
        read_response = self.client.post(
            self.CREATE_CLIENT,
            data=payload,
            format='json',
        )
        return read_response

    def post_update_client(self, payload, client_id):
        read_response = self.client.put(
            f"{self.UPDATE_CLIENT}{client_id}/",
            data=payload,
            format='json',
        )
        return read_response

    def post_delete_client(self, client_id):
        read_response = self.client.delete(
            f"{self.DELETE_CLIENT}{client_id}/",
            format='json',
        )
        return read_response

    def post_create_message(self, payload):
        read_response = self.client.post(
            self.CREATE_MESSAGE,
            data=payload,
            format='json',
        )
        return read_response

    def assert_successful_response(self, response):
        self.assertEqual(200, response.status_code)

    def assert_successful_created_response(self, response):
        self.assertEqual(201, response.status_code)

    def assert_successfully_deleted_client_response(self, detail, response):
        self.assertEqual(204, response.status_code)
        self.assertEqual(detail, response.data)

    def assert_not_found_obj_response(self, response):
        self.assertEqual(404, response.status_code)
        self.assertEqual('Not found.', response.data.get('detail'))

    def assert_does_not_support_response(self, detail, response):
        self.assertEqual(404, response.status_code)
        self.assertEqual(detail, response.data.get('detail'))

    def assert_successful_get_clients_count(self, response, expected_clients: []):
        self.assertEqual(len(expected_clients), len(response.data))

    def assert_response_permission_denied_for_user(self, response):
        self.assertEqual(403, response.status_code)
        self.assertEqual("You do not have permission for this action!", response.data.get("detail"))

    def assert_get_client_payload(self, expected_client, actual_client):
        self.assertEqual(expected_client.id, actual_client.get("id"))
        self.assertEqual(expected_client.name, actual_client.get("name"))
        self.assertEqual(expected_client.client_type.client_type,
                         actual_client.get("client_type").get("client_type"))
        self.assertEqual(len(expected_client.industries.all()), len(actual_client.get("industries")))
        self.assertEqual(len(expected_client.contact_persons.all()), len(actual_client.get('contact_persons')))
        self.assertEqual(expected_client.user.id, actual_client.get("user"))

    def assert_get_client_equal_json_payload_fields(self, expected, actual):
        for field_name in ("id", "user", "name", "client_type"):
            self.assertEqual(expected.get(field_name), actual.get(field_name), msg=field_name)

        expected_contact_persons = sorted(expected.get("contact_persons", []), key=lambda i: i["name"])
        actual_contact_persons = sorted(actual.get("contact_persons", []), key=lambda i: i["name"])
        self.assertEqual(len(expected_contact_persons), len(actual_contact_persons))
        for expected_contact_persons, actual_contact_persons in zip(expected_contact_persons, actual_contact_persons):
            for field_name in ("name", "role", "phone_number", "email", "telegram"):
                self.assertEqual(expected_contact_persons.get(field_name),
                                 actual_contact_persons.get(field_name), msg=field_name)

        expected_industries = sorted(expected.get("industries", []), key=lambda i: i["name"])
        actual_industries = sorted(actual.get("industries", []), key=lambda i: i["name"])
        self.assertEqual(len(expected_industries), len(actual_industries))
        for expected_industries, actual_industries in zip(expected_industries, actual_industries):
            for field_name in ("id", "name"):
                self.assertEqual(expected_industries.get(field_name), actual_industries.get(field_name), msg=field_name)

        expected_messages = sorted(expected.get("messages", []), key=lambda i: i["id"])
        actual_messages = sorted(actual.get("messages", []), key=lambda i: i["id"])
        self.assertEqual(len(expected_messages), len(actual_messages))
        for expected_messages, actual_messages in zip(expected_messages, actual_messages):
            for field_name in ("id", "message", "client"):
                self.assertEqual(expected_messages.get(field_name), actual_messages.get(field_name), msg=field_name)

    def assert_create_client_equal_payload(self, expected, actual):
        for field_name in ("name", "user", "client_type"):
            self.assertEqual(expected.get(field_name), actual.get(field_name), msg=field_name)

        expected_contact_persons = sorted(expected.get("contact_persons", []), key=lambda i: i["name"])
        actual_contact_persons = sorted(actual.get("contact_persons", []), key=lambda i: i["name"])
        self.assertEqual(len(expected_contact_persons), len(actual_contact_persons))
        for expected_contact_persons, actual_contact_persons in zip(expected_contact_persons, actual_contact_persons):
            for field_name in ("name", "role", "phone_number", "email", "telegram"):
                self.assertEqual(expected_contact_persons.get(field_name),
                                 actual_contact_persons.get(field_name), msg=field_name)

        expected_industries = sorted(expected.get("industries", []), key=lambda i: i["name"])
        actual_industries = sorted(actual.get("industries", []), key=lambda i: i["name"])
        self.assertEqual(len(expected_industries), len(actual_industries))
        for expected_industries, actual_industries in zip(expected_industries, actual_industries):
            for field_name in ("id", "name"):
                self.assertEqual(expected_industries.get(field_name), actual_industries.get(field_name), msg=field_name)

    def assert_get_client_types_list(self, expected, actual):
        self.assertEqual(len(expected), len(actual))

        for client_type in range(len(expected)):
            self.assertEqual(expected[client_type].id, actual[client_type].get("id"))
            self.assertEqual(expected[client_type].client_type, actual[client_type].get("client_type"))

    def assert_get_industries_list(self, expected, actual):
        self.assertEqual(len(expected), len(actual))

        for industry in range(len(expected)):
            self.assertEqual(expected[industry].id, actual[industry].get("id"))
            self.assertEqual(expected[industry].name, actual[industry].get("name"))
