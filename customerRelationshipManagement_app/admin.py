from django.contrib import admin

# Register your models here.

from customerRelationshipManagement_app.models import Client, Contract, Event


class ClientAdmin(admin.ModelAdmin):

    list_display = ('id', 'lastName', 'email', 'companyName', 'salesContact_id')


class ContractAdmin(admin.ModelAdmin):

    list_display = ('id', 'salesContact', 'client', 'status')


class EventAdmin(admin.ModelAdmin):

    list_display = ('id', 'supportContact', 'eventStatus', 'attendees')


admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)