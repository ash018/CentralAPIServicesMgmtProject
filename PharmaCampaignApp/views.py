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


class Level4CampaignForApproval(viewsets.ModelViewSet):
    queryset = Campaign.objects.none()
    serializer_class = Level4CampaignApprovalSerializer

    # Endpoint for POST
    def create(self, request):
        pass

    # Endpoint for GET
    def list(self, request):
        try:
            levelCode = request.GET['LevCode']

            if levelCode is None or str(levelCode) == '':
                return {'StatusCode': '302', 'StatusMessage': 'Please provide levelCode parameter.'}

            result = Callsp_Level4CampaignForApproval(levelCode)
            response = {'StatusCode': '200', 'StatusMessage': result}
            return Response(response)

        except Exception as e:
            return {'StatusCode': '404', 'StatusMessage': 'Exception occured: ' + str(e)}

class Level5CampaignForApproval(viewsets.ModelViewSet):
    queryset = Campaign.objects.none()
    serializer_class = Level5CampaignApprovalSerializer

    # Endpoint for POST
    def create(self, request):
        pass

    # Endpoint for GET
    def list(self, request):
        try:
            levelCode = request.GET['LevCode']
            if levelCode is None or str(levelCode) == '':
                return {'StatusCode': '302', 'StatusMessage': 'Please provide levelCode parameter.'}

            result = Callsp_Level5CampaignForApproval(levelCode)
            response = {'StatusCode': '200', 'StatusMessage': result}
            return Response(response)

        except Exception as e:
            return {'StatusCode': '404', 'StatusMessage': 'Exception occured: ' + str(e)}

class Level6CampaignForApproval(viewsets.ModelViewSet):
    queryset = Campaign.objects.none()
    serializer_class = Level6CampaignApprovalSerializer

    # Endpoint for POST
    def create(self, request):
        pass

    # Endpoint for GET
    def list(self, request):
        try:
            levelCode = request.GET['LevCode']
            if levelCode is None or str(levelCode) == '':
                return {'StatusCode': '302', 'StatusMessage': 'Please provide levelCode parameter.'}

            result = Callsp_Level6CampaignForApproval(levelCode)
            response = {'StatusCode': '200', 'StatusMessage': result}
            return Response(response)

        except Exception as e:
            print(str(e))
            return {'StatusCode': '404', 'StatusMessage': 'Exception occured: ' + str(e)}

class Level7CampaignForApproval(viewsets.ModelViewSet):
    queryset = Campaign.objects.none()
    serializer_class = Level7CampaignApprovalSerializer

    # Endpoint for POST
    def create(self, request):
        pass

    # Endpoint for GET
    def list(self, request):
        try:
            levelCode = request.GET['LevCode']
            if levelCode is None or str(levelCode) == '':
                return {'StatusCode': '302', 'StatusMessage': 'Please provide levelCode parameter.'}

            result = Callsp_Level7CampaignForApproval(levelCode)
            response = {'StatusCode': '200', 'StatusMessage': result}
            return Response(response)

        except Exception as e:
            print(str(e))
            return {'StatusCode': '404', 'StatusMessage': 'Exception occured: ' + str(e)}
