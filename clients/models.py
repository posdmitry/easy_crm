from django.contrib.auth.models import User
from django.db import models

from clients_auth.models import CustomUser, Company


class Industries(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Industry"
        verbose_name_plural = "Industries"


class ClientType(models.Model):
    client_type = models.CharField(max_length=25)

    def __str__(self):
        return self.client_type

    class Meta:
        verbose_name = "Client type"
        verbose_name_plural = "Types of clients"


class Clients(models.Model):
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    industries = models.ManyToManyField(Industries)
    client_type = models.ForeignKey(ClientType, related_name='type_of_client', null=True, on_delete=models.SET_NULL)
    date_time_next_contact = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, related_name='user', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Client"


class Messages(models.Model):
    message = models.TextField()
    date_time_create = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Clients, related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        return f"Message bound with {self.client}"

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"


class ContactPerson(models.Model):
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField(max_length=30, blank=True)
    telegram = models.CharField(max_length=50, blank=True)
    client = models.ForeignKey(Clients, related_name='contact_persons', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Contact person"
        verbose_name_plural = "Contact persons"
