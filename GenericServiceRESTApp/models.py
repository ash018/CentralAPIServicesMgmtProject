from django.db import models
from django.db import connection
from django.db import connection, connections

from django.contrib.auth.models import Group, User

class UserInfo(models.Model):
    UserId = models.AutoField(primary_key=True)
    UserName = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'GN_UserInfo'

    def __str__(self):
        return '{}, {}'.format(self.UserName, self.Password)


class ServiceCategory(models.Model):
    CategoryId = models.AutoField(primary_key=True)
    CategoryDetails = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'GN_ServiceCategory'

    def __str__(self):
        return '{}, {}'.format(self.CategoryDetails)


class Product(models.Model):
    ProductId = models.AutoField(primary_key=True)
    ProductName = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'GN_Product'

    def __str__(self):
        return '{}, {}'.format(self.ProductName)


class ServiceCall(models.Model):
    CallTypeId = models.AutoField(primary_key=True)
    CallTypeDetails = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'GN_ServiceCall'

    def __str__(self):
        return '{}, {}'.format(self.CallTypeDetails)


class Territory(models.Model):
    Id = models.AutoField(primary_key=True, db_column='TerritoryId')
    Name = models.CharField(max_length=100, db_column='TerritoryName')
    Code = models.CharField(max_length=50, db_column='TerritoryCode')
    Notes = models.CharField(max_length=100, db_column='Notes')
    user = models.ForeignKey(User,db_column='EntryBy',on_delete=models.CASCADE)

    def __str__(self):
        return self.Name

    class Meta:
        managed = True
        db_table = 'Territory'

class MotorTechnician(models.Model):
    Id = models.AutoField(primary_key=True, db_column='TechnicianId', default='0')
    Name = models.CharField(max_length=100, db_column='TechnicianName', default='')
    Designation = models.CharField(max_length=100, db_column='Designation')
    StaffId = models.CharField(max_length=100, db_column='StaffId', default='',unique=True)
    TerritoryCode = models.ForeignKey(Territory, db_column='TerritoryCode', on_delete=models.CASCADE)
    MobileNo = models.CharField(max_length=20, db_column='MobileNo', default='')
    BloodGroup = models.CharField(max_length=20, db_column='BloodGroup')
    Notes = models.CharField(max_length=100, db_column='Notes')
    user = models.ForeignKey(User, db_column='SupervisorCode', on_delete=models.CASCADE, default=1)

    # added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.Name

    class Meta:
        managed = True
        db_table = 'MotorTechnician'


class ServiceDetails(models.Model):
    ServiceDetailsId = models.AutoField(primary_key=True)
    CustomerName = models.CharField(max_length=100)
    Mobile = models.CharField(max_length=20)
    TractorPurchaseDate = models.DateTimeField()
    HoursProvided = models.IntegerField()
    DateOfInstallation = models.DateTimeField()
    ServiceDemandDate = models.DateTimeField()
    ServiceStartDate = models.DateTimeField()
    ServiceEndDate = models.DateTimeField()
    ServiceIncome = models.FloatField()
    VisitDate = models.DateTimeField()
    MobileCreatedDT = models.DateTimeField()
    MobileEditedDT = models.DateTimeField()
    MobileLogCount = models.IntegerField()
    MobileId = models.IntegerField()
    ServerInsertDateTime = models.DateTimeField(auto_now_add=True)
    ServerUpdateDateTime = models.DateTimeField(auto_now=True)
    Rating = models.CharField(max_length=10)
    UserId = models.ForeignKey(UserInfo, db_column='UserId', on_delete=models.CASCADE)
    CategoryId = models.ForeignKey(ServiceCategory, db_column='CategoryId', on_delete=models.CASCADE)
    ProductId = models.ForeignKey(Product, db_column='ProductId', on_delete=models.CASCADE)
    CallTypeId = models.ForeignKey(ServiceCall, db_column='CallTypeId', on_delete=models.CASCADE)
    SupervisorCode = models.ForeignKey(User, db_column='SupervisorCode', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'GN_ServiceDetails'

    def __str__(self):
        return '{}, {}'.format(self.ServiceDetailsId, self.CustomerName)

def dictfetchall(cur):
    dataset = cur.fetchall()
    columns = [col[0] for col in cur.description]
    return [
        dict(zip(columns, row))
        for row in dataset
        ]

def GetTargetVsAchievementByUser(staffid, period):
    cur = connections['ServiceTrack'].cursor()
    cur.execute("""

SELECT * FROM
(

		SELECT
		   PivotTable.TechnicianId,
			PivotTable.StaffId,
			PivotTable.TechnicianName,
			PivotTable.IsVerify,
			ISNULL(PivotTable.WARRANTY, 0) AS WARRANTY,
			ISNULL(PivotTable.POSTWARRANTY, 0) AS POSTWARRANTY,
		   ISNULL(WarrantyService, 0) AS WarrantyServiceTarget,
		   ISNULL(PostWarrantyService, 0) AS PostWarrantyServiceTarget,
		   CASE WHEN PivotTable.IsVerify = -1 THEN 'SHOW'
				WHEN PivotTable.IsVerify = 0 AND  (ISNULL(PivotTable.WARRANTY, 0) + ISNULL(PivotTable.POSTWARRANTY, 0)) > 0 THEN 'SHOW'
				WHEN PivotTable.IsVerify = 0 AND  (ISNULL(PivotTable.WARRANTY, 0) + ISNULL(PivotTable.POSTWARRANTY, 0)) = 0 THEN 'HIDE'
				WHEN PivotTable.IsVerify = 1 THEN 'SHOW'
			END AS VisibilityStatus,
			TG.EntryDate
		FROM
		(
			  SELECT TechnicianId, StaffId, TechnicianName, CategoryDetails, IsVerify, COUNT(CategoryDetails) AS TotalService
			  FROM (

					  SELECT ui.UserName,
							   MT.TechnicianId
							   ,MT.StaffId
							  ,MT.TechnicianName
							  ,ISNULL(SD.IsVerify, -1) IsVerify
							  ,CASE WHEN SC.CategoryDetails IN ('Installation', 'Periodical Service', 'Warranty Service') THEN 'WARRANTY'
									WHEN SC.CategoryDetails IN ('Paid Service', 'Post Warranty Customer Service') THEN 'POSTWARRANTY'
								ELSE ''
							  END AS CategoryDetails
					  FROM [dbo].[GN_ServiceDetails] SD
					  RIGHT JOIN [dbo].[GN_UserInfo] UI ON SD.UserId = UI.UserId --WHERE ui.UserName = 'C10001'
					  INNER JOIN [dbo].[MotorTechnician] MT ON UI.UserName = MT.StaffId
					  LEFT JOIN [dbo].[GN_ServiceCategory] SC ON SD.CategoryId = SC.[CategoryId]
					  --WHERE SD.IsVerify = 1
					  --WHERE  MT.StaffId = 'C10001'
			  ) AS TAB
			  GROUP BY TechnicianId, StaffId, TechnicianName, CategoryDetails, IsVerify
		) as T
		PIVOT
		(
             SUM(TotalService)
             FOR CategoryDetails IN ([WARRANTY], [POSTWARRANTY])
		) AS PivotTable
		LEFT JOIN dbo.[Target] TG ON TG.TsaTsoStaffID = PivotTable.TechnicianId

) as T
WHERE StaffId = '""" + staffid + """' AND VisibilityStatus = 'SHOW' AND CONVERT(nvarchar(6), EntryDate, 112) = CONVERT(nvarchar(6), CAST('""" + period + """' AS DATE), 112)""")
    result = dictfetchall(cur)
    cur.close()
    return result
