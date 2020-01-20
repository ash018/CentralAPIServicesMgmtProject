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
from .serializer import RoleStgSerializer, RoleStgSerializer2
from rest_framework.renderers import JSONRenderer
import json
import datetime
from django.http import JsonResponse
from django.core import serializers

from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
#from django.core import serializers
from django.core.serializers import serialize
from functools import reduce

#https://django-doc-test1.readthedocs.io/en/stable-1.5.x/topics/db/queries.html

class LoginCheck(viewsets.ModelViewSet):
    
    queryset = Role.objects.all()
    role_class = RoleStgSerializer

    # Endpoint to receive image from mobile app
    def create(self, request):
        userId = request.POST.get('userId')
        password = request.POST.get('password')
        # userId = request.POST['userId']
        #password = request.POST['password']
        print ('userId ' + str(userId) + ' password ' + str(password))
        checkUser = UserManager.objects.filter(UserId = userId, Password = password).values('UserId','UserName','RoleId').using('MotorConstructionEquipment')
        print ('checkUser ---- > ' +str(len(checkUser)))

        if len(checkUser) > 0 :
            data = json.dumps(list(checkUser))
            response = {'StatusCode': '200', 'StatusMessage': str(data)}
            return Response(response,content_type="application/json")
        else:
            response = {'StatusCode': '203', 'StatusMessage': 'UserId/Password Error'}
            return Response(response,content_type="application/json")

        response = {'StatusCode': '200', 'StatusMessage': 'resend'}
        return Response(response,content_type="application/json")


    def list(self, request):
        queryset = Role.objects.all().values('id', 'Role').using('MotorConstructionEquipment')
        data = json.dumps(list(queryset))

        response = {'StatusCode': '200', 'StatusMessage': str(data)}
        print(response)
        return Response(response,content_type="application/json")


class EngAndSS (viewsets.ModelViewSet):
    queryset = Role.objects.all()
    role_class = RoleStgSerializer

    def list(self, request):
        test_ids = Role.objects.filter(pk__in=[2,3]).using('MotorConstructionEquipment')
        #queryset = UserManager.objects.filter(RoleId__in = test_ids).values('UserId','UserName').using('MotorConstructionEquipment')
        queryset = UserManager.objects.filter(RoleId__in=test_ids).values('RoleId', 'UserId', 'UserName', 'RoleId__RoleName', 'StaffId').using('MotorConstructionEquipment')
        #print(queryset)
        #data = json.dumps(list(queryset))

        data = json.dumps(list(queryset))
        response = {'StatusCode': '200', 'StatusMessage': str(data)}
        return Response(response, content_type="application/json")


class MecAndSpo(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    role_class = RoleStgSerializer

    def list(self, request):
        roleId = request.GET['RoleId'].strip()
        #request.GET['roleId'] .strip()
        print('Role Id -- > ' + str(roleId))
        print('request -- > ' + str(request))
        role = []
        if roleId == '1':
            role = Role.objects.filter(pk__in=[2,3]).using('MotorConstructionEquipment')
            queryset = UserManager.objects.filter(RoleId__in=role).values('RoleId', 'UserId', 'UserName', 'RoleId__RoleName', 'StaffId').using( 'MotorConstructionEquipment')
            print(queryset)
            data = json.dumps(list(queryset))
            response = {'StatusCode': '200', 'StatusMessage': str(data)}
            return Response(response, content_type="application/json")


        if roleId == '2':
            #role = Role.objects.filter(id=5).using('MotorConstructionEquipment')
            role = Role.objects.filter(pk__in=[5,3]).using('MotorConstructionEquipment')
            # queryset = UserManager.objects.filter(RoleId=role[0]).values('RoleId', 'UserId', 'UserName',
            #                                                              'RoleId__RoleName', 'StaffId').using('MotorConstructionEquipment')

            queryset = UserManager.objects.filter(RoleId__in=role).values('RoleId', 'UserId', 'UserName',
                                                                         'RoleId__RoleName', 'StaffId').using(
                'MotorConstructionEquipment')
            print(queryset)
            data = json.dumps(list(queryset))

            response = {'StatusCode': '200', 'StatusMessage': str(data)}
            return Response(response, content_type="application/json")
        if roleId == '3':
            #role = Role.objects.filter(id=4).using('MotorConstructionEquipment')
            role = Role.objects.filter(pk__in=[2, 4]).using('MotorConstructionEquipment')
            # queryset = UserManager.objects.filter(RoleId=role[0]).values('RoleId', 'UserId', 'UserName',
            #                                                              'RoleId__RoleName', 'StaffId').using(
            #     'MotorConstructionEquipment')

            queryset = UserManager.objects.filter(RoleId__in=role).values('RoleId', 'UserId', 'UserName','RoleId__RoleName', 'StaffId').using('MotorConstructionEquipment')
            print(queryset)
            data = json.dumps(list(queryset))

            response = {'StatusCode': '200', 'StatusMessage': str(data)}
            return Response(response, content_type="application/json")
        if roleId == '4' or roleId == '5':
            response = {'StatusCode': '200', 'StatusMessage': 'NoNeed'}
            return Response(response, content_type="application/json")

class SaveService (viewsets.ModelViewSet):
    queryset = Role.objects.all()
    role_class = RoleStgSerializer

    def create(self, request):
        entryBy = request.POST.get('entryBy')
        companyName = request.POST.get('companyName')
        owner = request.POST.get('owner')
        models = request.POST.get('model')
        chassis = request.POST.get('chassis')
        hrm = request.POST.get('hrm')
        remarks = request.POST.get('remarks')
        AssignedPerson = request.POST.get('assignList')
        ServiceTime = request.POST.get('DateTime')
        ContactPerson = request.POST.get('ContactPerson')
        ServiceType = request.POST.get('ServiceType')
        user = UserManager.objects.filter(UserId = entryBy).using('MotorConstructionEquipment')
        customer = Customer.objects.filter(CompanyName = companyName).using('MotorConstructionEquipment')

        userForRole = UserManager.objects.filter(UserId=entryBy).values('UserId', 'UserName', 'StaffId', 'RoleId').using('MotorConstructionEquipment')

        jobTime = ServiceTime.split(' ')
        jobD = jobTime[0].split('-')
        jobT = jobTime[1].split(':')

        print(" AssignedPerson -> "+ str(AssignedPerson))
        JDateTime = datetime.datetime(int(jobD[2]), int(jobD[1]), int(jobD[0]), int(jobT[0]), int(jobT[1]), 26, 423)
        #print('AssigenedPerson name -> ' + str(AssigenedPerson[0]))
        Status = 'N'
        Latitude = '0.0'
        Longitude = '0.0'
        sTime = datetime.datetime.now()
        selectedCus = ''
        if len(customer) == 0 :
            customer = Customer(CompanyName = companyName, EntryDate = sTime, EntryBy = user[0])
            customer.save()
            selectedCus = customer
        else :
            selectedCus = customer[0]

        service = Service(CompanyName = companyName, ContactPerson = owner, ContactPersonType = ContactPerson, ServiceTime = JDateTime, Model = models, Chassis = chassis, HRM = hrm, ServiceType = ServiceType, Remark = remarks, Latitude=Latitude, Longitude = Longitude, Status = Status, EntryDate = sTime, EntryBy = user[0], CustomerId = selectedCus)
        service.save()
        listed_string = AssignedPerson[1:-1].split(",")
        #print("AssignedPerson" + AssignedPerson)
        check = ''
        rolelist=[]
        for i in range(len(listed_string)):
            ToAssigned = UserManager.objects.filter(StaffId=listed_string[i].strip()).values('RoleId').using('MotorConstructionEquipment')[0]
            #print("-Role--" + str(ToAssigned['RoleId']))
            #print(type(ToAssigned['RoleId']))
            rolelist.append(ToAssigned['RoleId'])
        myset = set(rolelist)
        myList = list(myset)
        mySetLen = len(myset)

        for i in range(len(myList)):
            if len(myList) > 1 and myList[i] == 4 and myList[i+1] == 2:
                #print("-Role123--" + str(ToAssigned['RoleId']))
                check = 0
                break
            if len(myList) > 1 and myList[i] == 2 and myList[i+1] == 4:
                #print("-Role123--" + str(ToAssigned['RoleId']))
                check = 0
                break

            if myList[i]==2:
                check=1
            if myList[i]==4:
                check=0
            else:
                check=1
            break


        for i in range(len(listed_string)):
            Status = 'N'
            ColorStatus = 1
            AssigdPer = UserManager.objects.filter(StaffId=listed_string[i].strip()).all().using('MotorConstructionEquipment')[0]
            ServiceAssigned(ServiceId=service, From=user[0], To=AssigdPer, Status=Status, EntryDate=sTime,
                                EditDate=sTime, color=ColorStatus).save()

        #print("---check---" + check + " User Role " + userForRole[0]['RoleId'])
        if check == 1 and userForRole[0]['RoleId'] == 3:
            print("---Now I am Here---" )
            Status = 'Y'
            ColorStatus = '2'
            ServiceAssigned(ServiceId=service, From=user[0], To=user[0], Status=Status, EntryDate=sTime,
                            EditDate=sTime, color=ColorStatus).save()
        if userForRole[0]['RoleId'] == 2:
            Status = 'Y'
            ColorStatus = '1'
            ServiceAssigned(ServiceId=service, From=user[0], To=user[0], Status=Status, EntryDate=sTime,EditDate=sTime, color=ColorStatus).save()


        response = {'StatusCode': '200', 'StatusMessage': 'ok'}
        return Response(response, content_type="application/json")

class PendingSaveService(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleStgSerializer2

    def create(self, request):
        roleId = request.POST.get('roleId')
        userId = request.POST.get('userId')
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')

        print("roleId " + str(roleId) + " userId " + str(userId) + " startDate " + str(startDate) + " endDate " + str(endDate))

        sDate = datetime.datetime(int(startDate.split('-')[2]), int(startDate.split('-')[1]), int(startDate.split('-')[0]), 0, 0, 0, 000)
        eDate = datetime.datetime(int(endDate.split('-')[2]), int(endDate.split('-')[1]), int(endDate.split('-')[0]), 23, 59, 59, 000)
        print("sDate " + str(sDate) + " endDate " + str(eDate))

        serviceWithColor = []

        User = UserManager.objects.filter(UserId= str(userId)).using('MotorConstructionEquipment')
        UserId = UserManager.objects.filter(UserId= str(userId)).values('id').using('MotorConstructionEquipment')
        userService = []
        allService = []
        if str(userId) == 'admin':
            # allServiceAdmin = ServiceAssigned.objects.filter(EntryDate__range=(sDate, eDate)).order_by('-id').values('ServiceId',
            #                                                                                               'ServiceId__CompanyName',
            #                                                                                               'To__UserName',
            #                                                                                               'ServiceId__ContactPerson',
            #                                                                                               'ServiceId__ServiceTime',
            #                                                                                               'Status',
            #                                                                                               'To__RoleId__id',
            #                                                                                               'color').using('MotorConstructionEquipment')
            #
            # allServiceAdmin = allServiceAdmin.extra(select={'datestr': "to_char(ServiceId__ServiceTime, 'YYYY-MM-DD HH24:MI:SS')"})
            # adminList = list(allServiceAdmin)
            # adminTemp = []
            # for item in adminList:
            #     item['ServiceId__ServiceTime'] = str(item['ServiceId__ServiceTime'].strftime('%Y-%m-%d %H:%M'))
            #     adminTemp.append(item)

            #data = json.dumps(adminTemp)

            #To=User[0],
            allSer = ServiceAssigned.objects.filter( EntryDate__range=(sDate, eDate)).values(
                'ServiceId').order_by('-id').using('MotorConstructionEquipment')
            allServiceTo = ServiceAssigned.objects.filter(ServiceId__in=allSer).values('ServiceId',
                                                                                       'ServiceId__CompanyName',
                                                                                       'To__UserName',
                                                                                       'ServiceId__ContactPerson',
                                                                                       'ServiceId__ServiceTime',
                                                                                       'Status', 'To__RoleId__id',
                                                                                       'color', 'To').using(
                'MotorConstructionEquipment')

            allServiceTo = allServiceTo.extra(
                select={'datestr': "to_char(ServiceId__ServiceTime, 'YYYY-MM-DD HH24:MI:SS')"})
            myList = list(allServiceTo)
            temp = []
            maxColor = 0
            x = 0
            for item in myList:
                item['ServiceId__ServiceTime'] = str(item['ServiceId__ServiceTime'].strftime('%Y-%m-%d %H:%M'))

                color = []
                for ik in myList:
                    if item['ServiceId'] == ik['ServiceId']:
                        color.append(ik['color'])

                item['color'] = str(max(color))
                color.clear()
                temp.append(item)

            # showLis = []
            # if str(UserId[0]['id']) != '1':
            #     for it in temp:
            #         if int(it['To']) == int(UserId[0]['id']):
            #             showLis.append(it)

            #data = json.dumps(showLis)
            data = json.dumps(temp)



            response = {'StatusCode': '200', 'StatusMessage': data}
            return Response(response, content_type="application/json")    
        else :
            allSer = ServiceAssigned.objects.filter(To=User[0], EntryDate__range=(sDate, eDate)).values('ServiceId').order_by('-id').using('MotorConstructionEquipment')
            allServiceTo = ServiceAssigned.objects.filter(ServiceId__in=allSer).values('ServiceId', 'ServiceId__CompanyName', 'To__UserName', 'ServiceId__ContactPerson', 'ServiceId__ServiceTime', 'Status','To__RoleId__id','color', 'To').using('MotorConstructionEquipment')

            allServiceTo = allServiceTo.extra(select={'datestr': "to_char(ServiceId__ServiceTime, 'YYYY-MM-DD HH24:MI:SS')"})
            myList = list(allServiceTo)
            temp = []
            maxColor = 0
            x = 0
            for item in myList:
                item['ServiceId__ServiceTime'] = str(item['ServiceId__ServiceTime'].strftime('%Y-%m-%d %H:%M'))
                
                color = []
                for ik in myList:
                    if item['ServiceId'] == ik['ServiceId']:
                        color.append(ik['color'])    
                
                item['color'] = str(max(color))
                color.clear()
                temp.append(item)

            showLis = []
            if str(UserId[0]['id']) != '1':
                for it in temp:
                    if int(it['To']) == int(UserId[0]['id']):
                        showLis.append(it)

            data = json.dumps(showLis)
            response = {'StatusCode': '200', 'StatusMessage': data}
            return Response(response, content_type="application/json")

    def list(self, request):
        serviceId = request.GET['ServiceId'].strip()
        entryBy = request.GET['UserId'].strip()
        print("serviceId" + serviceId)
        queryset = Service.objects.filter(pk = int(serviceId)).values('id','CompanyName', 'ContactPerson', 'ContactPersonType', 'ServiceTime', 'Model', 'Chassis', 'HRM', 'ServiceType', 'Remark').using('MotorConstructionEquipment')
        #Test Commit
        userId = UserManager.objects.filter(UserId=str(entryBy)).using('MotorConstructionEquipment')[0]

        seId = Service.objects.filter(pk = int(serviceId)).using('MotorConstructionEquipment')
        assignedPerson = ServiceAssigned.objects.filter(ServiceId=seId[0], From=userId).values('To__UserName','To__RoleId__id').using('MotorConstructionEquipment')
        
        queryset = queryset.extra(select={'datestr': "to_char(ServiceTime, 'YYYY-MM-DD HH24:MI:SS')"})
        mylist = list(queryset)
        
        allPerson = ''
        i = 0
        #print(str(list(assignedPerson)))
        for pi in assignedPerson:
            if i < len(assignedPerson)-1:
                allPerson = allPerson + pi['To__UserName'] + ","
            else :
                allPerson = allPerson + pi['To__UserName']
            i = i+1    

        temp = []
        for item in mylist:
            item['ServiceTime'] = str(item['ServiceTime'].strftime('%Y-%m-%d %H:%M'))
            item['Assigned'] = allPerson
            temp.append(item)

        
        data = json.dumps(list(temp))
        #person= json.dumps(list(assignedPerson))
        print("Service Posted Data -> " + str(data))
        response = {'StatusCode': '200', 'StatusMessage': str(data)}
        return Response(response, content_type="application/json")


class ForwardToMecnSpo(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    role_class = RoleStgSerializer

    def create(self, request):
        enrtyBy = request.POST.get('entryBy')
        serviceId = request.POST.get('serviceId')
        AssignedPerson = request.POST.get('staffId')
        models = request.POST.get('model')
        chassis = request.POST.get('chassis')
        hrm = request.POST.get('hrm')
        remarks = request.POST.get('remarks')
        print("serviceId " + str(serviceId) + " enrtyBy " + str(enrtyBy) + " staffId " + str(AssignedPerson))
        #assignedPersion = UserManager.objects.filter(StaffId= str(staffId)).using('MotorConstructionEquipment')
        user = UserManager.objects.filter(UserId = str(enrtyBy)).using('MotorConstructionEquipment')

        userEntryBy = UserManager.objects.filter(UserId = str(enrtyBy)).values('RoleId').using('MotorConstructionEquipment')
        service = Service.objects.filter(pk = int(serviceId)).using('MotorConstructionEquipment')
        #print('---- LEN --- ' + str(type(AssignedPerson)))
        listed_string = AssignedPerson[1:-1].split(",")
        #print("----" + AssignedPerson + "---" + str(listed_string) + "---List person---" + str(len(AssignedPerson)))

        st = 'Y'
        sTime = datetime.datetime.now()
        Status = 'N'
        ServiceAssigned.objects.filter(ServiceId=service[0], Status='N', To=user[0]).using('MotorConstructionEquipment').update(Status=st, EditDate=sTime)
        check = 0
        empCheck = 0
        iCount = 0
        #print ("listed_string len - >> " + str(len(listed_string)))
        for emi in listed_string:
            #print('incomming Element  -> ' + str(emi.strip()))
            if str(emi.strip()) == '' and iCount < len(listed_string):
                empCheck = 1
                break
            else :
                 empCheck = 2   
            iCount = iCount + 1        


        #print("empCheck ->" + str(type(empCheck)))
        #print("empCheck ->" + str(empCheck))
        
        if empCheck == 2:
            for i in range(len(listed_string)):
                #AssigdPer = UserManager.objects.filter(StaffId=listed_string[i].strip()).all().using('MotorConstructionEquipment')[0]
                AssigdPer = UserManager.objects.filter(StaffId=listed_string[i].strip()).values('RoleId').using('MotorConstructionEquipment')[0]
                AssPerson = UserManager.objects.filter(StaffId=listed_string[i].strip()).using('MotorConstructionEquipment')[0]
                #userRole = UserManager.objects.filter(StaffId=listed_string[i].strip()).all().using('MotorConstructionEquipment')[0]
                #sAssign = ServiceAssigned.objects.filter(ServiceId=service[0], To=assignedPersion[0]).using('MotorConstructionEquipment')
                sAssign = ServiceAssigned.objects.filter(ServiceId=service[0], To=AssPerson).using('MotorConstructionEquipment')
                
                

                if len(sAssign) == 0:
                    ColorStatus = 1
                    ServiceAssigned(ServiceId=service[0], From=user[0], To=AssPerson, Status=Status,  EditDate=sTime, EntryDate=sTime, color=ColorStatus).save()

                if AssigdPer['RoleId'] != 4 and userEntryBy[0]['RoleId'] == 3: 
                    check = 1  

            if check == 1:
                ColorStatus = 2
                ServiceAssigned.objects.filter(ServiceId=service[0], To=user[0]).using('MotorConstructionEquipment').update(EditDate=sTime, color=ColorStatus)
        
        if empCheck  == 1:
            ColorStatus = 2
            ServiceAssigned.objects.filter(ServiceId=service[0], To=user[0]).using('MotorConstructionEquipment').update(EditDate=sTime, color=ColorStatus)


        response = {'StatusCode': '200', 'StatusMessage': {'successfully update the service.'}}
        return Response(response, content_type="application/json")

class JobDoneByMecnSpo(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    role_class = RoleStgSerializer

    def create(self, request):
        enrtyBy = request.POST.get('entryBy')
        serviceId = request.POST.get('serviceId')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        models = request.POST.get('model')
        chassis = request.POST.get('chassis')
        hrm = request.POST.get('hrm')
        remarks = request.POST.get('remarks')

        user = UserManager.objects.filter(UserId=str(enrtyBy)).using('MotorConstructionEquipment')
        service = Service.objects.filter(pk=int(serviceId)).using('MotorConstructionEquipment')
        #serviceList = ServiceAssigned.objects.filter(ServiceId = service[0]).values('To','To__RoleId__id').using('MotorConstructionEquipment')
        st = 'Y'
        sTime = datetime.datetime.now()
        useRole = UserManager.objects.filter(UserId=str(enrtyBy)).values('RoleId').using('MotorConstructionEquipment')[0]
        print('-----'+ str(useRole['RoleId']))
        if useRole['RoleId'] == 4:
            ServiceAssigned.objects.filter(ServiceId=service[0], Status='N', To=user[0]).using('MotorConstructionEquipment').update(Status=st, EditDate=sTime, color=2)
            

        if useRole['RoleId'] == 5:
            ServiceAssigned.objects.filter(ServiceId=service[0], Status='N', To=user[0]).using('MotorConstructionEquipment').update(Status=st, EditDate=sTime, color=3)
            for i in service:
                ServiceAssigned.objects.filter(ServiceId=i).using('MotorConstructionEquipment').update(Status=st, EditDate=sTime, color='3')

        srvStatus = 'Done'
        Latitude = latitude
        Longitude = longitude
        Service.objects.filter(pk=int(serviceId)).using('MotorConstructionEquipment').update(Status=srvStatus, Model=models, Chassis=chassis, HRM=hrm, Remark=remarks, Latitude=Latitude, Longitude=Longitude)
        response = {'StatusCode': '200', 'StatusMessage': {'Update Done of Service.'}}
        return Response(response, content_type="application/json")