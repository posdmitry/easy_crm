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
        fields = ('message', 'date_time_create')


class ClientsSerializer(serializers.ModelSerializer):
    contact_persons = ContactPersonSerializer(read_only=True, many=True)
    messages = MessagesSerializer(read_only=True, many=True)
    type = serializers.StringRelatedField()

    class Meta:
        model = Clients
        fields = '__all__'
        depth = 1

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if industry := self.initial_data.get("industries", None):
            attrs["industries"] = industry
        return attrs

    def create(self, validated_data):
        industries_data = validated_data.pop('industries')

        client = Clients.objects.create(**validated_data)

        for industry in industries_data:
            industry_obj = Industries.objects.get(name=industry["name"])
            client.industries.add(industry_obj)
        client.save()
        return client
