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
import boto3


# This is the first call where it will be decided to which url either on-prem or cloud url will be set as main API Call for image processing
class UploadToS3(viewsets.ModelViewSet):
    queryset = ''
    serializer_class = TaskSerializer

    def create(self, request):
        try:
            image = request.FILES.get('prescription_image')
            filename = image.name
            service = AmazonServices()
            imageFileName = service.UploadToS3('bucket-rxcamp-prescriptions-pictures', filename, image)
            response = {'StatusCode': '200', 'StatusMessage': 'Image uploaded successfully.', 'URL' : imageFileName}
            return Response(response)
        except Exception as e:
            response = {'StatusCode': '400', 'StatusMessage': 'Image cant be uploaded.', 'URL': 'NotFound'}
            return Response(response)


class AmazonServices:
    AWS_ACCESS_ID = 'AKIAJ3CVLNXI4T7COHIQ',
    AWS_SECRET_ACCESS_KEY = '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'
    S3FileDownloadLink = ''
    def __init__(self):
        pass

    def UploadToS3(self, bucketName, S3FileName, fileToUpload):
        try:
            print('Uploading')
            s3 = boto3.resource('s3', aws_access_key_id = 'AKIAJ3CVLNXI4T7COHIQ', aws_secret_access_key = '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')
            s3.Bucket(bucketName).put_object(Key=S3FileName, Body=fileToUpload)
            object_acl = s3.ObjectAcl(bucketName, S3FileName)
            response = object_acl.put(ACL='public-read')
            self.S3FileDownloadLink = 'https://s3.amazonaws.com/' + bucketName + '/' + S3FileName
            return self.S3FileDownloadLink

        except Exception as e:
            print('Exception Occured: ' + str(e))
            return 'Not Found'
