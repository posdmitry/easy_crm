from clients_api.tests.base import ViewsBaseTestCase


class MessagesTestCase(ViewsBaseTestCase):
    API_VERSION = "/api/v1"
    CREATE_MESSAGE = f"{API_VERSION}/message/create/"

    def test_create_message_successful_by_admin(self):
        admin = self.get_test_user(**self.admin_user)
        client_admin = self.build_client(user=admin)
        self.client.force_authenticate(user=admin)

        payload = {
            "message": "Test message Hello!",
            "client": client_admin.id
        }

        response = self.post_create_message(payload=payload)
        self.assert_successful_created_response(response)

    def test_create_message_denied_by_admin(self):
        admin = self.get_test_user(**self.admin_user)
        strange_employee_user = self.get_test_user(**self.strange_employee_user)

        client_strange_employee = self.build_client(user=strange_employee_user)

        payload = {
            "message": "Test message Hello!",
            "client": client_strange_employee.id
        }

        self.client.force_authenticate(user=admin)
        response = self.post_create_message(payload=payload)
        self.assert_response_permission_denied_for_user(response)

    def test_create_message_successful_by_employee(self):
        employee = self.get_test_user(**self.employee_user)
        client_employee = self.build_client(user=employee)
        self.client.force_authenticate(user=employee)

        payload = {
            "message": "Test message Hello!",
            "client": client_employee.id
        }

        response = self.post_create_message(payload=payload)
        self.assert_successful_created_response(response)

    def test_create_message_denied_by_employee(self):
        employee = self.get_test_user(**self.employee_user)
        admin = self.get_test_user(**self.admin_user)

        client_admin = self.build_client(user=admin)

        payload = {
            "message": "Test message Hello!",
            "client": client_admin.id
        }

        self.client.force_authenticate(user=employee)
        response = self.post_create_message(payload=payload)
        self.assert_response_permission_denied_for_user(response)

    def test_create_message_denied_by_unknown_user(self):
        unknown_user = self.get_test_user()
        admin = self.get_test_user(**self.admin_user)

        client_admin = self.build_client(user=admin)

        payload = {
            "message": "Test message Hello!",
            "client": client_admin.id
        }

        self.client.force_authenticate(user=unknown_user)
        response = self.post_create_message(payload=payload)
        self.assert_response_permission_denied_for_user(response)