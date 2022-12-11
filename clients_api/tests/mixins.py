from clients_auth.models import CustomUser


class AuthenticatedTestClientMixin:

    """
    Automatically authenticates test.client.
    """

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.login()

    def get_test_user(self, *args, **kwargs):
        user, _ = CustomUser.objects.get_or_create(
            username=kwargs.get("username", "testUser"),
        )
        return user

    def login(self):
        self.client.force_authenticate(user=self.get_test_user())

    def logout(self):
        self.client.force_authenticate(user=None)