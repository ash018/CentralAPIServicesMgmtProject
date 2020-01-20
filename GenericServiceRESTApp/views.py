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
import json

# Create your views here.
class LoginViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    def create(self, request):
        user = request.POST['Username']
        pwd = request.POST['Password']
        obj = UserInfo.objects.filter(UserName = user, Password = pwd).using('ServiceTrack')
        if len(list(obj.values())) > 0:
            response = {'StatusCode': '200', 'StatusMessage': 'Login Successful'}
        else:
            response = {'StatusCode': '400', 'StatusMessage': 'Bad request. Login credentials are not valid'}
        return Response(response)


class ServiceDetailsViewSet(viewsets.ModelViewSet):
    queryset = ServiceDetails.objects.all()
    serializer_class = ServiceDetailsSerializer

    def create(self, request):
        try:
            userid = str(request.data.get('UserId'))
            data = json.loads(request.data.get('Data'))
            print(data)
            print(userid)
            for elem in data:
                print("======"+str(elem))
                TractorPurchaseDate = datetime.strptime(str(elem['KEY_BUYING_DATE']), '%Y-%m-%d %H:%M:%S')
                DateOfInstallation = datetime.strptime(str(elem['KEY_INSTALLAION_DATE']), '%Y-%m-%d %H:%M:%S')
                ServiceDemandDate = datetime.strptime(str(elem['KEY_CALL_SERVICE_DATE']), '%Y-%m-%d %H:%M:%S')
                ServiceStartDate = datetime.strptime(str(elem['KEY_SERVICE_START_DATE']), '%Y-%m-%d %H:%M:%S')
                ServiceEndDate = datetime.strptime(str(elem['KEY_SERVICE_END_DATE']), '%Y-%m-%d %H:%M:%S')
                VisitDate = datetime.strptime(str(elem['KEY_VISITED_DATE']), '%Y-%m-%d %H:%M:%S')
                MobileCreatedDT = datetime.strptime(str(elem['KEY_CREATED_AT']), '%Y-%m-%d %H:%M:%S')
                MobileEditedDT = datetime.strptime(str(elem['KEY_EDITED_AT']), '%Y-%m-%d %H:%M:%S')
                MobileId = int(elem['KEY_ID'])

                user_key = UserInfo.objects.filter(UserName=userid).using('ServiceTrack')
                service_category_key = ServiceCategory.objects.filter(CategoryId=int(elem['KEY_SERVICE_TYPE'])).using('ServiceTrack')
                product_key = Product.objects.filter(ProductId=int(elem['KEY_PRODUCT'])).using('ServiceTrack')
                service_call_key = ServiceCall.objects.filter(CallTypeId=int(elem['KEY_CALL_TYPE'])).using('ServiceTrack')

                data_mobile = ServiceDetails.objects.filter(MobileId=MobileId, UserId=user_key[0]).using('ServiceTrack')
                #print("======XXXXXXXXX========="+str(data_mobile))
                if len(list(data_mobile.values())) > 0: #Update operation
                    print('Update Ope')
                    data_mobile = data_mobile[0]
                    data_mobile.CustomerName = str(elem['KEY_CUSTOMER_NAME'])
                    data_mobile.Mobile = str(elem['KEY_CUSTOMER_MOBILE'])
                    data_mobile.TractorPurchaseDate = datetime.strptime(str(elem['KEY_BUYING_DATE']), '%Y-%m-%d %H:%M:%S')
                    data_mobile.HoursProvided = int(elem['KEY_RUNNING_HOUER'])
                    data_mobile.DateOfInstallation = datetime.strptime(str(elem['KEY_INSTALLAION_DATE']), '%Y-%m-%d %H:%M:%S')
                    data_mobile.ServiceDemandDate = datetime.strptime(str(elem['KEY_CALL_SERVICE_DATE']), '%Y-%m-%d %H:%M:%S')
                    data_mobile.ServiceStartDate = datetime.strptime(str(elem['KEY_SERVICE_START_DATE']), '%Y-%m-%d %H:%M:%S')
                    data_mobile.ServiceEndDate = datetime.strptime(str(elem['KEY_SERVICE_END_DATE']), '%Y-%m-%d %H:%M:%S')
                    data_mobile.ServiceIncome = float(elem['KEY_SERVICE_INCOME'])
                    data_mobile.VisitDate = datetime.strptime(str(elem['KEY_VISITED_DATE']), '%Y-%m-%d %H:%M:%S')
                    data_mobile.MobileCreatedDT = datetime.strptime(str(elem['KEY_CREATED_AT']), '%Y-%m-%d %H:%M:%S')
                    data_mobile.MobileEditedDT = datetime.strptime(str(elem['KEY_EDITED_AT']), '%Y-%m-%d %H:%M:%S')
                    data_mobile.MobileLogCount = int(elem['KEY_EDIT_LOG_COUNT'])
                    data_mobile.MobileId = MobileId
                    data_mobile.UserId = user_key[0]
                    data_mobile.CategoryId = service_category_key[0]
                    data_mobile.ProductId = product_key[0]
                    data_mobile.CallTypeId = service_call_key[0]
                    data_mobile.save(using='ServiceTrack')

                else:   #Insert operation
                    #motTechnicianObj = MotorTechnician.objects.filter(StaffId=userid).first().using('ServiceTrack')
                    print("====== Insert Ops")
                    supeCode = MotorTechnician.objects.filter(StaffId=userid).values('user').order_by('user').using('ServiceTrack')[0]
                    supervisorCode = User.objects.filter(pk=int(supeCode['user'])).using('ServiceTrack')[0]
                    print("===XXX===" + str(supeCode))

                    # obj = ServiceDetails(CustomerName=str(elem['KEY_CUSTOMER_NAME']), Mobile=str(elem['KEY_CUSTOMER_MOBILE']), TractorPurchaseDate=TractorPurchaseDate,
                    #                      HoursProvided=int(elem['KEY_RUNNING_HOUER']), DateOfInstallation=DateOfInstallation, ServiceDemandDate=ServiceDemandDate,
                    #                      ServiceStartDate=ServiceStartDate, ServiceEndDate=ServiceEndDate, ServiceIncome=float(elem['KEY_SERVICE_INCOME']),VisitDate=VisitDate,
                    #                      MobileCreatedDT=MobileCreatedDT, MobileEditedDT=MobileEditedDT, MobileLogCount=int(elem['KEY_EDIT_LOG_COUNT']), MobileId=MobileId,
                    #                      UserId=user_key[0], CategoryId=service_category_key[0], ProductId=product_key[0], CallTypeId=service_call_key[0])

                    obj = ServiceDetails(CustomerName=str(elem['KEY_CUSTOMER_NAME']),
                                         Mobile=str(elem['KEY_CUSTOMER_MOBILE']),
                                         TractorPurchaseDate=TractorPurchaseDate,
                                         HoursProvided=int(elem['KEY_RUNNING_HOUER']),
                                         DateOfInstallation=DateOfInstallation, ServiceDemandDate=ServiceDemandDate,
                                         ServiceStartDate=ServiceStartDate, ServiceEndDate=ServiceEndDate,
                                         ServiceIncome=float(elem['KEY_SERVICE_INCOME']), VisitDate=VisitDate,
                                         MobileCreatedDT=MobileCreatedDT, MobileEditedDT=MobileEditedDT,
                                         MobileLogCount=int(elem['KEY_EDIT_LOG_COUNT']), MobileId=MobileId,
                                         Rating=str(elem['KEY_RATING']),
                                         UserId=user_key[0],
                                         CategoryId=service_category_key[0],
                                         ProductId=product_key[0],
                                         CallTypeId=service_call_key[0],
                                         SupervisorCode=supervisorCode)
                    obj.save(using='ServiceTrack')

            return Response({'StatusCode': '200', 'StatusMessage': 'Service Added Successfully'})

            # try:
            #     CustomerName = str(request.POST['CustomerName'])
            # except:
            #     CustomerName = 'NA'
            #
            # try:
            #     Mobile = str(request.POST['Mobile'])
            # except:
            #     Mobile = 'NA'
            #
            # try:
            #     TractorPurchaseDate = datetime.strptime(str(request.POST['TractorPurchaseDate']), '%Y-%m-%d %H:%M:%S')
            # except:
            #     TractorPurchaseDate = datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
            #
            # try:
            #     HoursProvided = int(request.POST['HoursProvided'])
            # except:
            #     HoursProvided = 0
            #
            # try:
            #     DateOfInstallation = datetime.strptime(str(request.POST['DateOfInstallation']), '%Y-%m-%d %H:%M:%S')
            # except:
            #     DateOfInstallation = datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
            #
            #
            # try:
            #     ServiceDemandDate = datetime.strptime(str(request.POST['ServiceDemandDate']), '%Y-%m-%d %H:%M:%S')
            # except:
            #     ServiceDemandDate = datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
            #
            # try:
            #     ServiceStartDate = datetime.strptime(str(request.POST['ServiceStartDate']), '%Y-%m-%d %H:%M:%S')
            # except:
            #     ServiceStartDate = datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
            #
            # try:
            #     ServiceEndDate = datetime.strptime(str(request.POST['ServiceEndDate']), '%Y-%m-%d %H:%M:%S')
            # except:
            #     ServiceEndDate = datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
            #
            # try:
            #     ServiceIncome = float(request.POST['ServiceIncome'])
            # except:
            #     ServiceIncome = 0
            #
            # try:
            #     VisitDate = datetime.strptime(str(request.POST['VisitDate']), '%Y-%m-%d %H:%M:%S')
            # except:
            #     VisitDate = datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

            # try:
            #     CategoryId = int(request.POST['CategoryId'])
            # except:
            #     CategoryId = 1
            #
            # try:
            #     ProductId = int(request.POST['ProductId'])
            # except:
            #     ProductId = 1
            #
            # try:
            #     CallTypeId = int(request.POST['CallTypeId'])
            # except:
            #     CallTypeId = 1



            # if CategoryId == 1: #Installation
            #     obj = ServiceDetails(CustomerName=CustomerName, Mobile=Mobile, TractorPurchaseDate=TractorPurchaseDate,HoursProvided=HoursProvided, DateOfInstallation=DateOfInstallation,
            #                          CategoryId = service_category_key[0], ProductId=product_key[0], CallTypeId=service_call_key[0])
            #     obj.save(using='ServiceTrack')
            #
            #
            # if CategoryId == 2 or CategoryId == 3: #Periodical Service
            #     obj = ServiceDetails(CustomerName=CustomerName, Mobile=Mobile, HoursProvided=HoursProvided, ServiceDemandDate=ServiceDemandDate, ServiceStartDate=ServiceStartDate, ServiceEndDate=ServiceEndDate,
            #                          CategoryId=service_category_key[0], ProductId=product_key[0], CallTypeId=service_call_key[0])
            #     obj.save(using='ServiceTrack')
            #
            # if CategoryId == 4: #Paid Service
            #     obj = ServiceDetails(CustomerName=CustomerName, Mobile=Mobile, HoursProvided=HoursProvided, ServiceDemandDate=ServiceDemandDate, ServiceStartDate=ServiceStartDate, ServiceEndDate=ServiceEndDate, ServiceIncome=ServiceIncome,
            #                          CategoryId=service_category_key[0], ProductId=product_key[0], CallTypeId=service_call_key[0])
            #     obj.save(using='ServiceTrack')
            #
            # if CategoryId == 5: #Paid Service
            #     obj = ServiceDetails(CustomerName=CustomerName, Mobile=Mobile, HoursProvided=HoursProvided, VisitDate=VisitDate,
            #                          CategoryId=service_category_key[0], ProductId=product_key[0], CallTypeId=service_call_key[0])
            #     obj.save(using='ServiceTrack')

        except Exception as ex:
            return Response({'StatusCode': '500', 'StatusMessage': 'Exception Occured. Details: ' + str(ex)})


class GetUserServiceViewSet(viewsets.ModelViewSet):
    queryset = ServiceDetails.objects.all()
    serializer_class = ServiceDetailsSerializer
    def create(self, request):
        try:
            userid = str(request.data.get('UserId'))
            user_key = UserInfo.objects.filter(UserName=userid).using('ServiceTrack')
            obj = ServiceDetails.objects.filter(UserId=user_key[0]).using('ServiceTrack').order_by('MobileId')
            data = list(obj.values())
            return Response({'StatusCode': '200', 'StatusMessage': data})
        except Exception as ex:
            return Response({'StatusCode': '500', 'StatusMessage': 'Exception Occured. Details: ' + str(ex)})


class GetUserServiceViewSet(viewsets.ModelViewSet):
    queryset = ServiceDetails.objects.all()
    serializer_class = ServiceDetailsSerializer
    def create(self, request):
        try:
            userid = str(request.data.get('UserId'))
            #MotorTechnician.objects.filter(StaffId=userid).using('ServiceTrack')
            user_key = UserInfo.objects.filter(UserName=userid).using('ServiceTrack')
            obj = ServiceDetails.objects.filter(UserId=user_key[0]).using('ServiceTrack').order_by('MobileId')
            data = list(obj.values())
            return Response({'StatusCode': '200', 'StatusMessage': data})
        except Exception as ex:
            return Response({'StatusCode': '500', 'StatusMessage': 'Exception Occured. Details: ' + str(ex)})


class GetTargetVsAchievement(viewsets.ModelViewSet):
    queryset = ServiceDetails.objects.all()
    serializer_class = ServiceDetailsSerializer
    def create(self, request):
        try:
            staffid = str(request.data.get('UserId'))
            period = str(request.data.get('Period'))
            #MotorTechnician.objects.filter(StaffId=userid).using('ServiceTrack')
            result = GetTargetVsAchievementByUser(staffid, period)
            #print(result)
            ##Only for Kallul Vai's purpose, I am returning results like this way
            if len(result) == 0:
                return Response({'StatusCode': '400', 'StatusMessage': []})
            else:
                return Response({'StatusCode': '200', 'StatusMessage': result})
        except Exception as ex:
            return Response({'StatusCode': '500', 'StatusMessage': 'Exception Occured. Details: ' + str(ex)})