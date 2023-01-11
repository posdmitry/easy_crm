from clients_api.tests.base import ViewsBaseTestCase
from clients_api.tests.factories import ClientTypeFactory, IndustriesFactory, ContactPersonFactory


class ClientsTestCase(ViewsBaseTestCase):
    API_VERSION = "/api/v1"
    LIST_CLIENTS = f"{API_VERSION}/clients/"
    RETRIEVE_CLIENT = f"{API_VERSION}/clients/"
    CREATE_CLIENT = f"{API_VERSION}/clients/create/"
    UPDATE_CLIENT = f"{API_VERSION}/clients/update/"
    DELETE_CLIENT = f"{API_VERSION}/clients/delete/"
    LIST_CLIENT_TYPES = f"{API_VERSION}/client_types/"
    LIST_INDUSTRIES = f"{API_VERSION}/industries/"

    def test_get_list_clients(self):
        user = self.get_test_user()
        admin = self.get_test_user(**self.admin_user)
        employee = self.get_test_user(**self.employee_user)
        superuser = self.get_test_user(**self.superuser)

        expected_clients = list()
        expected_clients.append(self.build_client(user=user))
        expected_clients.append(self.build_client(user=admin))
        expected_clients.append(self.build_client(user=employee))
        expected_clients.append(self.build_client(user=superuser))

        self.client.force_authenticate(user=superuser)
        response = self.get_list_clients_request()

        self.assert_successful_response(response)
        self.assert_successful_get_clients_count(response, expected_clients)

    def test_get_list_clients_by_unknown_user(self):
        admin = self.get_test_user(**self.admin_user)
        employee = self.get_test_user(**self.employee_user)
        superuser = self.get_test_user(**self.superuser)
        unknown_user = self.get_test_user()

        self.build_client(user=admin)
        self.build_client(user=employee)
        self.build_client(user=superuser)

        self.client.force_authenticate(user=unknown_user)
        response = self.get_list_clients_request()
        self.assert_response_permission_denied_for_user(response)

    def test_get_list_clients_by_strange_user(self):
        admin = self.get_test_user(**self.admin_user)
        employee = self.get_test_user(**self.employee_user)
        strange_employee = self.get_test_user(**self.strange_employee_user)

        self.build_client(user=admin)
        self.build_client(user=strange_employee)
        expected_client = self.build_client(user=employee)

        self.client.force_authenticate(user=employee)
        response = self.get_list_clients_request()
        self.assert_successful_response(response)
        self.assert_get_client_payload(expected_client=expected_client, actual_client=response.data[0])

    def test_get_list_clients_by_admin_user(self):
        admin = self.get_test_user(**self.admin_user)
        employee = self.get_test_user(**self.employee_user)
        strange_employee = self.get_test_user(**self.strange_employee_user)

        expected_clients = list()
        expected_clients.append(self.build_client(user=admin))
        expected_clients.append(self.build_client(user=employee))
        self.build_client(user=strange_employee)

        self.client.force_authenticate(user=admin)
        response = self.get_list_clients_request()
        self.assert_successful_response(response)
        self.assert_get_client_payload(expected_client=expected_clients[0], actual_client=response.data[0])
        self.assert_successful_get_clients_count(response, expected_clients)

    def test_get_retrieve_client_by_unknown_user(self):
        admin = self.get_test_user(**self.admin_user)
        unknown_user = self.get_test_user()

        client = self.build_client(user=admin)

        self.client.force_authenticate(user=unknown_user)
        response = self.get_retrieve_client_request(client.id)
        self.assert_response_permission_denied_for_user(response)

    def test_get_retrieve_client_by_employee_user(self):
        admin = self.get_test_user(**self.admin_user)
        employee = self.get_test_user(**self.employee_user)

        client_admin = self.build_client(user=admin)
        client_employee = self.build_client(user=employee)

        self.client.force_authenticate(user=employee)
        response = self.get_retrieve_client_request(client_employee.id)
        self.assert_successful_response(response)

        forbidden_response = self.get_retrieve_client_request(client_admin.id)
        self.assert_not_found_obj_response(forbidden_response)

    def test_get_retrieve_client_by_admin_user(self):
        admin = self.get_test_user(**self.admin_user)
        employee = self.get_test_user(**self.employee_user)
        strange_employee_user = self.get_test_user(**self.strange_employee_user)

        client_admin = self.build_client(user=admin)
        client_employee = self.build_client(user=employee)
        client_strange_employee = self.build_client(user=strange_employee_user)

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

        client_admin = self.build_client(user=admin)
        client_employee = self.build_client(user=employee)
        client_strange_employee = self.build_client(user=strange_employee_user)

        self.client.force_authenticate(user=strange_employee_user)
        response_employees_client = self.get_retrieve_client_request(client_employee.id)
        response_admin_client = self.get_retrieve_client_request(client_admin.id)
        response_strange_employee_client = self.get_retrieve_client_request(client_strange_employee.id)

        self.assert_successful_response(response_strange_employee_client)
        self.assert_not_found_obj_response(response_employees_client)
        self.assert_not_found_obj_response(response_admin_client)

    def test_get_retrieve_equal_payload(self):
        admin = self.get_test_user(**self.admin_user)
        client_admin = self.build_client(user=admin)
        self.client.force_authenticate(user=admin)

        contact_persons = client_admin.contact_persons.all()
        messages = client_admin.messages.all()
        industries = client_admin.industries.all()

        expected_result = {
            "id": client_admin.id,
            "contact_persons": [{
                "name": contact_person.name,
                "role": contact_person.role,
                "phone_number": contact_person.phone_number,
                "email": contact_person.email,
                "telegram": contact_person.telegram,
            } for contact_person in contact_persons],
            "messages": [{
                "id": message.id,
                "message": message.message,
                "client": message.client.id,
            } for message in messages],
            "user": client_admin.user.id,
            "name": client_admin.name,
            "client_type": {
                "id": client_admin.client_type.id,
                "client_type": client_admin.client_type.client_type
            },
            "industries": [{
                "id": industry.id,
                "name": industry.name,
            } for industry in industries],
        }

        response = self.get_retrieve_client_request(client_admin.id)
        self.assert_successful_response(response)
        self.assert_get_client_equal_json_payload_fields(expected=expected_result, actual=response.json())
        self.assert_get_client_payload(expected_client=client_admin, actual_client=response.data)

    def test_create_client_successful_with_name_field_only(self):
        admin = self.get_test_user(**self.admin_user)

        self.client.force_authenticate(user=admin)

        payload = {
            "name": "Test Client!"
        }

        response = self.post_create_client(payload=payload)
        self.assert_successful_created_response(response)

    def test_create_client_successful_with_existent_client_type(self):
        admin = self.get_test_user(**self.admin_user)
        cl_type = ClientTypeFactory(client_type='client')

        self.client.force_authenticate(user=admin)

        payload = {
            "name": "Test Client!",
            "client_type": cl_type.id
        }

        expected_result = {
            "name": payload["name"],
            "client_type": {
                "id": cl_type.id,
                "client_type": cl_type.client_type
            },
            "industries": [],
            "contact_persons": [],
            "user": admin.id,
        }

        response = self.post_create_client(payload=payload)
        self.assert_successful_created_response(response)
        self.assert_create_client_equal_payload(expected=expected_result, actual=response.json())

    def test_create_client_with_client_type_does_not_support(self):
        admin = self.get_test_user(**self.admin_user)

        self.client.force_authenticate(user=admin)

        payload = {
            "name": "Test Client!",
            "client_type": 1
        }

        response = self.post_create_client(payload=payload)
        self.assert_does_not_support_response(detail="Client type does not support!", response=response)

    def test_create_client_successful_with_existent_industries(self):
        admin = self.get_test_user(**self.admin_user)
        cl_type = ClientTypeFactory(client_type='client')
        industries = IndustriesFactory.create_batch(3)

        self.client.force_authenticate(user=admin)

        payload = {
            "name": "Test Client!",
            "client_type": cl_type.id,
            "industries": [
                {
                    "id": industries[0].id,
                    "name":  industries[0].name,
                },
                {
                    "id": industries[1].id,
                    "name": industries[1].name,
                },
                {
                    "id": industries[2].id,
                    "name": industries[2].name,
                }
            ]
        }

        expected_result = {
            "name": payload["name"],
            "client_type": {
                "id": cl_type.id,
                "client_type": cl_type.client_type
            },
            "industries": [
                {
                    "id": industries[0].id,
                    "name": industries[0].name,
                },
                {
                    "id": industries[1].id,
                    "name": industries[1].name,
                },
                {
                    "id": industries[2].id,
                    "name": industries[2].name,
                }
            ],
            "contact_persons": [],
            "user": admin.id,
        }

        response = self.post_create_client(payload=payload)
        self.assert_successful_created_response(response)
        self.assert_create_client_equal_payload(expected=expected_result, actual=response.json())

    def test_create_client_successful_with_existent_contact_person(self):
        admin = self.get_test_user(**self.admin_user)
        cl_type = ClientTypeFactory(client_type='client')
        industries = IndustriesFactory.create_batch(3)

        self.client.force_authenticate(user=admin)

        payload = {
            "name": "Test Client!",
            "client_type": cl_type.id,
            "industries": [
                {
                    "id": industries[0].id,
                    "name":  industries[0].name,
                },
                {
                    "id": industries[1].id,
                    "name": industries[1].name,
                },
                {
                    "id": industries[2].id,
                    "name": industries[2].name,
                }
            ],
            "contact_persons": [
                {
                    "name": "Vova",
                    "role": "SEO",
                    "phone_number": "0670000000",
                    "email": "mail@t.com",
                    "telegram": "@vova"
                },
                {
                    "name": "Sasha",
                    "role": "manager",
                    "phone_number": "0680000000",
                    "email": "sasha@t.com",
                    "telegram": "@sasha"
                }
            ]
        }

        expected_result = {
            "name": payload["name"],
            "client_type": {
                "id": cl_type.id,
                "client_type": cl_type.client_type
            },
            "industries": [
                {
                    "id": industries[0].id,
                    "name": industries[0].name,
                },
                {
                    "id": industries[1].id,
                    "name": industries[1].name,
                },
                {
                    "id": industries[2].id,
                    "name": industries[2].name,
                }
            ],
            "contact_persons": [
                {
                    "name": "Vova",
                    "role": "SEO",
                    "phone_number": "0670000000",
                    "email": "mail@t.com",
                    "telegram": "@vova"
                },
                {
                    "name": "Sasha",
                    "role": "manager",
                    "phone_number": "0680000000",
                    "email": "sasha@t.com",
                    "telegram": "@sasha"
                }
            ],
            "user": admin.id,
        }

        response = self.post_create_client(payload=payload)
        self.assert_successful_created_response(response)
        self.assert_create_client_equal_payload(expected=expected_result, actual=response.json())

    def test_update_self_client_by_admin_successful_with_name_field_only(self):
        admin = self.get_test_user(**self.admin_user)
        client_admin = self.build_client(user=admin)

        self.client.force_authenticate(user=admin)

        payload = {
            "id": client_admin.id,
            "name": "Test Client!"
        }

        response = self.post_update_client(payload=payload, client_id=client_admin.id)
        self.assert_successful_response(response)
        self.assertEqual(payload["name"], response.json().get("name"))

    def test_update_employees_client_by_admin_successful_with_name_field_only(self):
        admin = self.get_test_user(**self.admin_user)
        employee = self.get_test_user(**self.employee_user)
        client_employee = self.build_client(user=employee)

        self.client.force_authenticate(user=admin)

        payload = {
            "id": client_employee.id,
            "name": "Test Client!"
        }

        response = self.post_update_client(payload=payload, client_id=client_employee.id)
        self.assert_successful_response(response)
        self.assertEqual(payload["name"], response.json().get("name"))

    def test_update_admins_client_by_employee_forbidden_with_name_field_only(self):
        admin = self.get_test_user(**self.admin_user)
        employee = self.get_test_user(**self.employee_user)
        client_admin = self.build_client(user=admin)

        self.client.force_authenticate(user=employee)

        payload = {
            "id": client_admin.id,
            "name": "Test Client!"
        }

        response = self.post_update_client(payload=payload, client_id=client_admin.id)
        self.assert_not_found_obj_response(response)

    def test_update_strangers_client_by_admin_forbidden_with_name_field_only(self):
        admin = self.get_test_user(**self.admin_user)
        strange_employee_user = self.get_test_user(**self.strange_employee_user)
        client_strange_employee = self.build_client(user=strange_employee_user)

        self.client.force_authenticate(user=admin)

        payload = {
            "id": client_strange_employee.id,
            "name": "Test Client!"
        }

        response = self.post_update_client(payload=payload, client_id=client_strange_employee.id)
        self.assert_not_found_obj_response(response)

    def test_update_employees_client_by_unknown_user_forbidden_with_name_field_only(self):
        employee = self.get_test_user(**self.employee_user)
        unknown_user = self.get_test_user()
        client_employee = self.build_client(user=employee)

        self.client.force_authenticate(user=unknown_user)

        payload = {
            "id": client_employee.id,
            "name": "Test Client!"
        }

        response = self.post_update_client(payload=payload, client_id=client_employee.id)
        self.assert_response_permission_denied_for_user(response)

    def test_update_self_client_successful_with_all_fields(self):
        admin = self.get_test_user(**self.admin_user)
        client_admin = self.build_client(user=admin)

        self.client.force_authenticate(user=admin)

        cl_type = ClientTypeFactory(client_type='cold')
        industries = IndustriesFactory.create_batch(2)

        payload = {
            "name": "Test Client!",
            "client_type": cl_type.id,
            "industries": [
                {
                    "id": industries[0].id,
                    "name": industries[0].name,
                },
                {
                    "id": industries[1].id,
                    "name": industries[1].name,
                }
            ],
            "contact_persons": [
                {
                    "name": "Vova",
                    "role": "SEO",
                    "phone_number": "0670000000",
                    "email": "mail@t.com",
                    "telegram": "@vova"
                },
                {
                    "id": client_admin.contact_persons.all()[0].id,
                    "name": "Test Contact Person Name",
                    "role": "test_role",
                    "phone_number": "test0670000000",
                    "email": "test@test.com",
                    "telegram": "@test",
                    "client_id": client_admin.contact_persons.all()[0].client_id
                }
            ]
        }

        expected_result = {
            "id": client_admin.id,
            "name": payload["name"],
            "client_type": {
                "id": cl_type.id,
                "client_type": cl_type.client_type
            },
            "industries": [
                {
                    "id": industries[0].id,
                    "name": industries[0].name,
                },
                {
                    "id": industries[1].id,
                    "name": industries[1].name,
                }
            ],
            "contact_persons": [
                {
                    "name": "Vova",
                    "role": "SEO",
                    "phone_number": "0670000000",
                    "email": "mail@t.com",
                    "telegram": "@vova"
                },
                {
                    "name": "Test Contact Person Name",
                    "role": "test_role",
                    "phone_number": "test0670000000",
                    "email": "test@test.com",
                    "telegram": "@test"
                }
            ],
            "user": admin.id,
        }

        response = self.post_update_client(payload=payload, client_id=client_admin.id)
        self.assert_successful_response(response)
        self.assert_get_client_equal_json_payload_fields(expected=expected_result, actual=response.json())

    def test_successfully_deleted_self_client_by_admin(self):
        admin = self.get_test_user(**self.admin_user)
        client_admin = self.build_client(user=admin)

        self.client.force_authenticate(user=admin)

        response = self.post_delete_client(client_admin.id)
        self.assert_successfully_deleted_client_response(
            detail=f"Client with id={client_admin.id} has successfully deleted!",
            response=response
        )

    def test_successfully_deleted_self_client_by_employee(self):
        employee = self.get_test_user(**self.employee_user)
        client_employee = self.build_client(user=employee)

        self.client.force_authenticate(user=employee)

        response = self.post_delete_client(client_employee.id)
        self.assert_successfully_deleted_client_response(
            detail=f"Client with id={client_employee.id} has successfully deleted!",
            response=response
        )

    def test_successfully_deleted_employees_client_by_admin(self):
        admin = self.get_test_user(**self.admin_user)
        employee = self.get_test_user(**self.employee_user)
        client_employee = self.build_client(user=employee)

        self.client.force_authenticate(user=admin)

        response = self.post_delete_client(client_employee.id)
        self.assert_successfully_deleted_client_response(
            detail=f"Client with id={client_employee.id} has successfully deleted!",
            response=response
        )

    def test_forbidden_deleted_admins_client_by_employee(self):
        admin = self.get_test_user(**self.admin_user)
        employee = self.get_test_user(**self.employee_user)
        client_admin = self.build_client(user=admin)

        self.client.force_authenticate(user=employee)

        response = self.post_delete_client(client_admin.id)
        self.assert_not_found_obj_response(response)

    def test_forbidden_deleted_client_by_unknown_user(self):
        unknown_user = self.get_test_user()
        employee = self.get_test_user(**self.employee_user)
        client_employee = self.build_client(user=employee)

        self.client.force_authenticate(user=unknown_user)

        response = self.post_delete_client(client_employee.id)
        self.assert_response_permission_denied_for_user(response)

    def test_client_types_list(self):
        user = self.get_test_user()
        self.client.force_authenticate(user=user)

        expected_client_types = self.build_client_types()
        response = self.get_list_client_types_request()
        self.assert_successful_response(response)
        self.assert_get_client_types_list(expected=expected_client_types, actual=response.json())

    def test_industries_list(self):
        user = self.get_test_user()
        self.client.force_authenticate(user=user)

        expected_industries = self.build_industries()
        response = self.get_list_industries()
        self.assert_successful_response(response)
        self.assert_get_industries_list(expected=expected_industries, actual=response.json())






