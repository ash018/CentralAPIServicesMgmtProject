from rest_framework import serializers

from .models import *

class RoleStgSerializer(serializers.ModelSerializer):
    json = serializers.SerializerMethodField('clean_json')
    class Meta:
        model = Role
        fields = ('id', 'Role')

class RoleStgSerializer2(serializers.ModelSerializer):
    #json = serializers.SerializerMethodField('clean_json')
    class Meta:
        model = Role
        fields = ('id', 'Role')


class UserManagerStgSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserManager
        fields = ('UserId', 'UserName', 'Password')



