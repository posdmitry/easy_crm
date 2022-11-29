from django.contrib import admin

from clients.models import Clients, ClientType, Industries, Messages, ContactPerson


class MessagesInline(admin.TabularInline):
    model = Messages
    extra = 0
    readonly_fields = ('date_time_create', 'message')


class ContactPersonsInline(admin.TabularInline):
    model = ContactPerson
    extra = 0
    readonly_fields = ('role',)


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    fields = (('name', 'date_time_next_contact'), ('industries', 'type'))
    list_display = ('name', 'type', 'date_time_next_contact')
    inlines = [ContactPersonsInline, MessagesInline]


@admin.register(ClientType)
class ClientTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Industries)
class IndustriesAdmin(admin.ModelAdmin):
    pass


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('date_time_create', 'client', 'message')


@admin.register(ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    list_display = ('client', 'name', 'phone_number')
