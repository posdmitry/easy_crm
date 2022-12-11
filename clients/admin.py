from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from clients.models import Clients, ClientType, Industries, Messages, ContactPerson
from clients_auth.models import CustomUser, Company


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name", "is_staff", "company")
    custom_fieldsets = (
        ('Company settings', {
            'fields': ('company', 'is_admin', 'is_employee', )
        }),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets = fieldsets + self.custom_fieldsets
        return fieldsets


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


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
    fieldsets = (
        ('Owner', {
            'fields': ('get_company', 'user')
        }),
        ('General information', {
            'fields': (('name', 'date_time_next_contact'), ('industries', 'client_type'),)
        })
    )
    list_display = ('id', 'name', 'client_type', 'date_time_next_contact', 'get_company', 'user')
    inlines = [ContactPersonsInline, MessagesInline]
    readonly_fields = ('get_company',)

    def get_company(self, obj):
        return obj.user.company

    get_company.short_description = 'Owner company'

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request)
        if not request.user.is_superuser:
            fields += ('user',)
        return fields

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)


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
