from django.db import models
from django.db import connection, connections
import json
from datetime import datetime
from sqlserver_ado.fields import LegacyDateTimeField
import urllib3
import urllib.request

class DocumentItem(models.Model):
    DocumentItemId = models.AutoField(db_column='DocumentItemId', primary_key=True)
    DocumentName = models.CharField(max_length=255, db_column='DocumentName')
    SortOrder = models.IntegerField(db_column='SortOrder')
    EntryDate = models.DateTimeField()
    Category = models.CharField(max_length=10, db_column='Category')
    class Meta:
        managed = False
        db_table = 'DocumentItem'

class RegistrationType(models.Model):
    RegisterTypeId = models.AutoField(db_column='RegisterTypeId', primary_key=True)
    RegisterTypeName = models.CharField(max_length=255, db_column='RegisterTypeName')
    EntryDate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'RegistrationType'


class UserPanel(models.Model):
    UserId = models.AutoField(db_column='UserId', primary_key=True)
    UserInvoiceNo = models.CharField(max_length=255, db_column='UserInvoiceNo')
    UserName = models.CharField(max_length=255, db_column='UserName')
    Password = models.CharField(max_length=255, db_column='Password')
    Status = models.IntegerField(db_column='Status')
    EntryDate = models.DateTimeField()
    RegisterTypeId = models.ForeignKey(RegistrationType, db_column='RegisterTypeId', on_delete=models.CASCADE)
    DeviceToken = models.CharField(max_length=512, db_column='DeviceToken')

    class Meta:
        managed = False
        db_table = 'UserPanel'


class RegistrationStatus(models.Model):
    RegistrationStatusId = models.AutoField(db_column='RegistrationStatusId', primary_key=True)
    UserId = models.ForeignKey(UserPanel, db_column='UserId', on_delete=models.CASCADE)
    DocumentItemId = models.ForeignKey(DocumentItem, db_column='DocumentItemId', on_delete=models.CASCADE)
    InvoiceNo = models.CharField(max_length=25, db_column='InvoiceNo')
    Status = models.CharField(max_length=5, db_column='Status')
    EntryDate = models.DateTimeField()
    EntryBy = models.CharField(max_length=25, db_column='EntryBy')
    RegisterTypeId = models.ForeignKey(RegistrationType, db_column='RegisterTypeId', on_delete=models.CASCADE)
    class Meta:
        managed = False
        db_table = 'RegistrationStatus'


class Invoice(models.Model):
    InvoiceNo = models.CharField(max_length=11, db_column='InvoiceNo', primary_key=True)
    InvoiceDate = models.CharField(max_length=30, db_column='InvoiceDate')
    CustomerCode = models.CharField(max_length=7, db_column='CustomerCode')
    CustomerName = models.CharField(max_length=50, db_column='CustomerName')
    ContactPerson = models.CharField(max_length=50, db_column='ContactPerson')
    Mobile = models.CharField(max_length=100, db_column='Mobile')
    ChasisNo = models.CharField(max_length=100, db_column='ChasisNo')
    EngineNo = models.CharField(max_length=100, db_column='EngineNo')

    class Meta:
        managed = False
        db_table = 'vwInvoice'