from clients_api.tests.base import ViewsBaseTestCase
from clients_auth.models import Company


class ClientSerializerTestCase(ViewsBaseTestCase):
    API_VERSION = "/api/v1"
    LIST_CLIENTS = f"{API_VERSION}/clients/"
    RETRIEVE_CLIENT = f"{API_VERSION}/clients/"
    CREATE_CLIENT = ""
    LIST_MESSAGES = ""
    CREATE_MESSAGE = ""

    def setUp(self, *args, **kwargs):
        self.company, _ = Company.objects.get_or_create(name='TestCompany')
        self.strange_company, _ = Company.objects.get_or_create(name='Strange Company')
        self.admin_user = {'username': 'testUser1', 'company': self.company, 'is_admin': True}
        self.employee_user = {'username': 'testUser2', 'company': self.company, 'is_employee': True}
        self.strange_employee_user = {'username': 'testUser3', 'company': self.strange_company, 'is_employee': True}
        self.superuser = {'username': 'testUser3', 'is_superuser': True}
        super().setUp()

    def test_get_list_clients(self):
        user = self.get_test_user()
        admin = self.get_test_user(**self.admin_user)
        employee = self.get_test_user(**self.employee_user)
        superuser = self.get_test_user(**self.superuser)

        expected_clients = list()
        expected_clients.append(self.buid_client(user=user))
        expected_clients.append(self.buid_client(user=admin))
        expected_clients.append(self.buid_client(user=employee))
        expected_clients.append(self.buid_client(user=superuser))

        self.client.force_authenticate(user=superuser)
        response = self.get_list_clients_request()

        self.assert_successful_response(response)
        self.assert_successful_get_clients_count(response, expected_clients)

    def test_get_list_clients_by_unknown_user(self):
        admin = self.get_test_user(**self.admin_user)
        employee = self.get_test_user(**self.employee_user)
        superuser = self.get_test_user(**self.superuser)
        unknown_user = self.get_test_user()

        self.buid_client(user=admin)
        self.buid_client(user=employee)
        self.buid_client(user=superuser)

        self.client.force_authenticate(user=unknown_user)
        response = self.get_list_clients_request()
        self.assert_response_unknown_user(response)

    def test_get_list_clients_by_strange_user(self):
        admin = self.get_test_user(**self.admin_user)
        employee = self.get_test_user(**self.employee_user)
        strange_employee = self.get_test_user(**self.strange_employee_user)

        self.buid_client(user=admin)
        self.buid_client(user=strange_employee)
        expected_client = self.buid_client(user=employee)

        self.client.force_authenticate(user=employee)
        response = self.get_list_clients_request()
        self.assert_successful_response(response)
        self.assert_client_payload(response.data[0], expected_client)

    def test_get_list_clients_by_admin_user(self):
        admin = self.get_test_user(**self.admin_user)
        employee = self.get_test_user(**self.employee_user)
        strange_employee = self.get_test_user(**self.strange_employee_user)

        expected_clients = list()
        expected_clients.append(self.buid_client(user=admin))
        expected_clients.append(self.buid_client(user=employee))
        self.buid_client(user=strange_employee)

        self.client.force_authenticate(user=admin)
        response = self.get_list_clients_request()
        self.assert_successful_response(response)
        self.assert_client_payload(response.data[0], expected_clients[0])
        self.assert_successful_get_clients_count(response, expected_clients)

    def test_get_retrieve_client_by_unknown_user(self):
        admin = self.get_test_user(**self.admin_user)
        unknown_user = self.get_test_user()

        client = self.buid_client(user=admin)

        self.client.force_authenticate(user=unknown_user)
        response = self.get_retrieve_client_request(client.id)
        self.assert_response_unknown_user(response)

    def test_get_retrieve_client_by_employee_user(self):
        admin = self.get_test_user(**self.admin_user)
        employee = self.get_test_user(**self.employee_user)

        client_admin = self.buid_client(user=admin)
        client_employee = self.buid_client(user=employee)

        self.client.force_authenticate(user=employee)
        response = self.get_retrieve_client_request(client_employee.id)
        self.assert_successful_response(response)

        forbidden_response = self.get_retrieve_client_request(client_admin.id)
        self.assert_not_found_obj_response(forbidden_response)

    def test_get_retrieve_client_by_admin_user(self):
        admin = self.get_test_user(**self.admin_user)
        employee = self.get_test_user(**self.employee_user)
        strange_employee_user = self.get_test_user(**self.strange_employee_user)

        client_admin = self.buid_client(user=admin)
        client_employee = self.buid_client(user=employee)
        client_strange_employee = self.buid_client(user=strange_employee_user)

        self.client.force_authenticate(user=admin)
        response_employees_client = self.get_retrieve_client_request(client_employee.id)
        response_admin_client = self.get_retrieve_client_request(client_admin.id)
        forbidden_response = self.get_retrieve_client_request(client_strange_employee.id)

        self.assert_successful_response(response_employees_client)
        self.assert_successful_response(response_admin_client)
        self.assert_not_found_obj_response(forbidden_response)

    def test_get_retrieve_client_by_strange_user(self):
        admin = self.get_test_user(**self.admin_user)
        employee = self.get_test_user(**self.employee_user)
        strange_employee_user = self.get_test_user(**self.strange_employee_user)

        client_admin = self.buid_client(user=admin)
        client_employee = self.buid_client(user=employee)
        client_strange_employee = self.buid_client(user=strange_employee_user)

        self.client.force_authenticate(user=strange_employee_user)
        response_employees_client = self.get_retrieve_client_request(client_employee.id)
        response_admin_client = self.get_retrieve_client_request(client_admin.id)
        response_strange_employee_client = self.get_retrieve_client_request(client_strange_employee.id)

        self.assert_successful_response(response_strange_employee_client)
        self.assert_not_found_obj_response(response_employees_client)
        self.assert_not_found_obj_response(response_admin_client)








