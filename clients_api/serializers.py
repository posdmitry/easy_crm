from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers
from clients.models import Clients, Industries, ContactPerson, Messages, ClientType
from rest_framework.exceptions import PermissionDenied, NotFound

from clients_auth.models import CustomUser


class IndustriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Industries
        fields = ('id', 'name',)


class ClientTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientType
        fields = ('id', 'client_type',)


class ContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPerson
        fields = ('name', 'role', 'phone_number', 'email', 'telegram')


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = "__all__"


class CreateMessageSerializer(serializers.ModelSerializer):
    """
    Create messages serializer and validation
    """
    class Meta:
        model = Messages
        fields = ('message', 'client',)

    def validate_client(self, attrs):
        attrs = super().validate(attrs)
        user = self.context.get('request').user

        if user.is_admin and not user.company_id == attrs.user.company_id:
            raise PermissionDenied(detail="You do not have permission for this action!")
        elif user.is_employee and not user.id == attrs.user.id:
            raise PermissionDenied(detail="You do not have permission for this action!")
        elif not user.is_admin and not user.is_employee and not user.is_superuser:
            raise PermissionDenied(detail="You do not have permission for this action!")
        else:
            return attrs


class ClientsSerializer(serializers.ModelSerializer):
    contact_persons = ContactPersonSerializer(read_only=True, many=True)
    industries = IndustriesSerializer(read_only=True, many=True)
    messages = MessagesSerializer(read_only=True, many=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Clients
        fields = '__all__'
        depth = 1


class ClientsListSerializer(ClientsSerializer):
    """
    Serialize list of clients
    """
    class Meta:
        model = Clients
        fields = ('id', 'name', 'client_type', 'industries', 'contact_persons', 'date_time_next_contact', 'user')
        depth = 1


class ClientCreateSerializer(ClientsSerializer):
    """
    Serialize for client creating
    """
    client_type = ClientTypeSerializer(read_only=True)

    class Meta:
        model = Clients
        fields = ('id', 'name', 'client_type', 'industries', 'contact_persons', 'user')

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if client_type := self.initial_data.get("client_type", None):
            attrs["client_type"] = client_type
        if industries := self.initial_data.get("industries", []):
            attrs["industries"] = industries
        if contact_persons := self.initial_data.get("contact_persons", []):
            attrs["contact_persons"] = contact_persons
        return attrs

    def create(self, validated_data):
        industries_data = validated_data.pop("industries", [])
        contact_persons_data = validated_data.pop("contact_persons", [])
        client_type = validated_data.pop("client_type", None)

        user = self.context.get("request").user.id
        validated_data["user"] = CustomUser.objects.get(pk=user)

        client = Clients.objects.create(**validated_data)

        if client_type:
            try:
                client_type_instance = ClientType.objects.get(pk=client_type)
                client.client_type = client_type_instance
            except ObjectDoesNotExist:
                raise NotFound("Client type does not support!")

        if industries_data:
            for industry in industries_data:
                try:
                    industry_obj = Industries.objects.get(pk=industry["id"])
                except ObjectDoesNotExist:
                    raise NotFound(f"Industry '{industry['name']}' does not support!")
                client.industries.add(industry_obj)

        if contact_persons_data:
            for contact_person in contact_persons_data:
                contact_person["client_id"] = client.pk
                contact_person_obj = ContactPerson.objects.create(**contact_person)
                client.contact_persons.add(contact_person_obj)

        client.save()
        return client

class ClientUpdateSerializer(ClientCreateSerializer):
    """
    Serialize for client update
    """
    client_type = ClientTypeSerializer(read_only=True)

    class Meta:
        model = Clients
        fields = ('id', 'name', 'client_type', 'industries', 'contact_persons', 'user')

    @staticmethod
    def _update_contact_persons(instance, contact_persons_data):
        contact_persons_to_update = []
        contact_persons_to_create = []

        for contact_person in contact_persons_data:
            contact_person["client_id"] = instance.pk

            if "id" in contact_person:
                contact_persons_to_update.append(ContactPerson(**contact_person))
            else:
                contact_persons_to_create.append(ContactPerson(**contact_person))

        ContactPerson.objects.\
            filter(client_id=instance.pk).\
            exclude(pk__in=[c.pk for c in contact_persons_to_update]).\
            delete()

        if contact_persons_to_create:
            ContactPerson.objects.bulk_create(contact_persons_to_create)

        if contact_persons_to_update:
            ContactPerson.objects.bulk_update(contact_persons_to_update,
                                              ["name", "role", "phone_number", "email", "telegram"])

    @transaction.atomic()
    def update(self, instance, validated_data):
        industries_data = validated_data.pop("industries", [])
        contact_persons_data = validated_data.pop("contact_persons", [])
        client_type = validated_data.pop("client_type", None)

        if client_type:
            try:
                client_type_instance = ClientType.objects.get(pk=client_type)
                instance.client_type = client_type_instance
            except ObjectDoesNotExist:
                raise NotFound("Client type does not support!")

        if industries_data:
            instance.industries.clear()
            for industry in industries_data:
                try:
                    industry_obj = Industries.objects.get(pk=industry["id"])
                except ObjectDoesNotExist:
                    raise NotFound(f"Industry '{industry['name']}' does not support!")
                instance.industries.add(industry_obj)

        self._update_contact_persons(instance=instance, contact_persons_data=contact_persons_data)
        instance = super().update(instance, validated_data)

        return instance








