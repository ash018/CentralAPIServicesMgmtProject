from django.db import models
from django.db import connection, connections
import json
from datetime import datetime
from sqlserver_ado.fields import LegacyDateTimeField
import urllib3
import urllib.request

class Campaign(models.Model):
    CampaignId = models.AutoField(primary_key=True)
    CampaignName = models.CharField(max_length=255)
    EntryBy = models.CharField(max_length=100)
    StartDate = models.DateTimeField(auto_now_add=True)
    EndDate = models.DateTimeField(auto_now_add=True)
    IsActive = models.CharField(max_length=10)
    EntryDate = models.DateTimeField(auto_now_add=True)
    EditDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'Campaign'

def dictfetchall(cur):
    dataset = cur.fetchall()
    columns = [col[0] for col in cur.description]
    return [
        dict(zip(columns, row))
        for row in dataset
        ]

def Callsp_Level4CampaignForApproval(levelCode):
    cur = connections['PharmaCampaign'].cursor()
    query = "exec [dbo].[sp_Level4CampaignForApproval] '" + str(levelCode) + "'"
    cur.execute(query)
    result = dictfetchall(cur)
    cur.close()
    return result

def Callsp_Level5CampaignForApproval(levelCode):
    cur = connections['PharmaCampaign'].cursor()
    query = "exec [dbo].[sp_Level5CampaignForApproval] '" + str(levelCode) + "'"
    cur.execute(query)
    result = dictfetchall(cur)
    cur.close()
    return result

def Callsp_Level6CampaignForApproval(levelCode):
    cur = connections['PharmaCampaign'].cursor()
    query = "exec [dbo].[sp_Level6CampaignForApproval] '" + str(levelCode) + "'"
    cur.execute(query)
    result = dictfetchall(cur)
    cur.close()
    return result

def Callsp_Level7CampaignForApproval(levelCode):
    cur = connections['PharmaCampaign'].cursor()
    query = "exec [dbo].[sp_Level7CampaignForApproval] '" + str(levelCode) + "'"
    cur.execute(query)
    result = dictfetchall(cur)
    cur.close()
    return result

# def Test():
#     cur = connections['PharmaCampaign'].cursor()
#     query = "SELECT  * FROM [dbo].[Campaign]"
#     cur.execute(query)
#     result = dictfetchall(cur)
#     cur.close()
#     return result
