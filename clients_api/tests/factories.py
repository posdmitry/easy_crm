import factory
from dateutil.tz import tzutc
from django.utils.datetime_safe import datetime
from django.contrib.auth.hashers import make_password
from factory import post_generation
from faker import Factory

from clients.models import Industries, ClientType, ContactPerson, Clients
from clients_auth.models import CustomUser, Company


fake = Factory.create()


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker('name')


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    company = factory.SubFactory(CompanyFactory)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('username')
    password = factory.LazyFunction(lambda: make_password('password'))
    is_staff = True
    is_superuser = True
    is_admin = False
    is_employee = True


class IndustriesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Industries

    # name = factory.Faker('pystr')
    name = factory.Iterator(['Metal', 'Foam', 'Food', 'Bio Fuel', 'Slate'])


class ClientTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClientType

    client_type = factory.Iterator(['client', 'cold', 'potential', 'warm'])


class ClientsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Clients

    name = factory.Faker('name')
    date_created = factory.LazyFunction(datetime.now)
    date_modified = factory.LazyAttribute(lambda f: str(fake.date_time(tzinfo=tzutc())))
    client_type = factory.SubFactory(ClientTypeFactory)
    date_time_next_contact = factory.LazyAttribute(lambda f: str(fake.date_time(tzinfo=tzutc())))
    user = factory.SubFactory(CustomUserFactory)

    @post_generation
    def industries(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.industries.add(*extracted)


class ContactPersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContactPerson

    name = factory.Faker('name')
    role = factory.Iterator(['SEO', 'Manager'])
    phone_number = factory.Faker('phone_number')
    email = factory.Faker('email')
    telegram = factory.Iterator(['@test', '@test1'])
    client = factory.SubFactory(ClientsFactory)
