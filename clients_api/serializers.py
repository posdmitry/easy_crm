from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from clients.models import Clients, Industries, ContactPerson, Messages


class IndustriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Industries
        fields = ('name',)


class ContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPerson
        fields = ('name', 'role', 'phone_number', 'email', 'telegram')


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = "__all__"


class ClientsSerializer(serializers.ModelSerializer):
    contact_persons = ContactPersonSerializer(read_only=True, many=True)
    messages = MessagesSerializer(read_only=True, many=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Clients
        fields = '__all__'
        depth = 1

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if industry := self.initial_data.get("industries", None):
            attrs["industries"] = industry
        if contact_persons := self.initial_data.get("contact_persons", None):
            attrs["contact_persons"] = contact_persons
        return attrs

    def create(self, validated_data):
        industries_data = validated_data.pop("industries", {})
        contact_persons_data = validated_data.pop("contact_persons", {})

        client = Clients.objects.create(**validated_data)

        for industry in industries_data:
            try:
                industry_obj = Industries.objects.get(name=industry["name"])
            except ObjectDoesNotExist:
                raise ValueError(f"Industry '{industry['name']}' does not support!")
            client.industries.add(industry_obj)
        for contact_person in contact_persons_data:
            contact_person["client_id"] = client.pk
            contact_person_obj = ContactPerson.objects.create(**contact_person)
            client.contact_persons.add(contact_person_obj)
        client.save()
        return client


class ClientsListSerializer(ClientsSerializer):
    """
    Serialize list of clients
    """
    class Meta:
        model = Clients
        fields = ('id', 'name', 'client_type', 'industries', 'contact_persons', 'date_time_next_contact', 'user')
        depth = 1
