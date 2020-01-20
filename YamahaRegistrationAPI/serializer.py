from rest_framework import serializers

from .models import *

class UserPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPanel
        fields = ('UserId', 'UserInvoiceNo', 'UserName', 'Password', 'Status', 'EntryDate', 'RegisterTypeId')

class RegistrationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationStatus
        fields = '__all__'