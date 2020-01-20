from django.shortcuts import render
from django.conf import settings
import django_filters
from rest_framework import viewsets, filters
from rest_framework.decorators import detail_route, list_route
from rest_framework.views import APIView
import os
from rest_framework.response import Response
from datetime import datetime
from .models import *
from rest_framework.reverse import reverse
from .serializer import *
from rest_framework.renderers import JSONRenderer
import json



class ValidateUser(viewsets.ModelViewSet):
    queryset = UserPanel.objects.all()
    serializer_class = UserPanelSerializer

    # Endpoint to receive image from mobile app
    def create(self, request):
        try:
            userid = request.POST['userId']
            password = request.POST['password']
            device_token = request.POST['device_token']
            user = UserPanel.objects.filter(UserInvoiceNo=userid, Password=password).using('YamahaRegistration')
            if len(user) == 0:
                response = {'StatusCode': '400', 'StatusMessage': [{'Message': 'Invalid username or password'}]}
                return Response(response)
            else:
                userList = list(user.values())
                token = userList[0]['DeviceToken']
                user[0].DeviceToken = device_token #if no device token is available for this user, update his device token
                user[0].save()
                response = {'StatusCode': '200', 'StatusMessage': [{'Message': 'Login successful!'}]}
                return Response(response)

        except Exception as e:
            return Response({'StatusCode': '500', 'StatusMessage': [{'Message':'Exception Occured:' + str(e)}]})

    def list(self, request):
        return None

class GetRegistrationStatus(viewsets.ModelViewSet):
    queryset = RegistrationStatus.objects.all()
    serializer_class = RegistrationStatusSerializer

    def list(self, request):
        userid = request.GET['userid'].strip()
        queryset = RegistrationStatus.objects.filter(InvoiceNo=userid).using('YamahaRegistration').values('RegistrationStatusId',
                                                                                       'UserId__UserName',
                                                                                       'DocumentItemId__DocumentName', 'DocumentItemId__Category',
                                                                                       'InvoiceNo', 'Status',
                                                                                       'EntryDate', 'RegisterTypeId')

        queryset = queryset.extra(select={'datestr': "to_char(EntryDate, 'YYYY-MM-DD HH24:MI:SS')"})
        dataset = list(queryset)

        if len(dataset) == 0:
            return Response({'StatusCode': '400', 'StatusMessage': 'Bad Request. No data found for this user.'}, content_type="application/json")

        customer = Invoice.objects.filter(InvoiceNo=userid).using('YamahaRegistration')
        customer = list(customer.values())
        isDeliverablesPanelVisible = "1"
        registrationType = 'ACI' if dataset[0]['RegisterTypeId'] == 1 else 'Self'
        if registrationType == 'ACI':
            for item in dataset:
                if item['Status'] == 'N':
                    isDeliverablesPanelVisible = "0"
                    break

            response = {'StatusCode': '200', 'RegistrationType': registrationType, 'ShowDeliverablesPanel': isDeliverablesPanelVisible, 'StatusMessage': dataset, 'CustomerInfo': [customer[0]]}
            return Response(response, content_type="application/json")
        else:
            deliveryStatus = 'Pending'
            for item in dataset:
                if item['DocumentItemId__Category'] == 'out' and item['EntryDate'] is not None:
                    deliveryStatus = item['EntryDate']
                    break
            response = {'StatusCode': '200', 'RegistrationType': registrationType, 'ShowDeliverablesPanel': isDeliverablesPanelVisible, 'StatusMessage': [deliveryStatus], 'CustomerInfo': [customer[0]]}
            return Response(response, content_type="application/json")
