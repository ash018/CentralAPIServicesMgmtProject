from django.db import models
from django.db import connection, connections
class Role(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    RoleName = models.CharField(max_length=50,db_column='RoleName')

    class Meta:
        managed = False
        db_table = 'Role'

    def __str__(self):
        return '{}, {}'.format(self.id, self.RoleName)

class UserManager(models.Model):
    id = models.AutoField(primary_key=True,db_column='id')
    UserId = models.CharField(max_length=50,db_column='UserId')
    UserName =  models.CharField(max_length=255,db_column='UserName')
    Password =  models.CharField(max_length=100,db_column='Password')
    StaffId = models.CharField(max_length=100, db_column='StaffId')
    EntryDate = models.DateTimeField(auto_now_add=True,db_column='EntryDate')
    RoleId = models.ForeignKey(Role, db_column='RoleId', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'UserManager'

    def __str__(self):
        return '{}, {}'.format(self.id, self.UserId, self.RoleId)


class Customer(models.Model):
    id = models.AutoField(primary_key=True, db_column='CustomerId')
    CompanyName =  models.CharField(max_length=255,db_column='CompanyName')
    EntryDate = models.DateTimeField(auto_now_add=True,db_column='EntryDate')
    EntryBy =  models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'Customer'

    def __str__(self):
        return '{}, {}'.format(self.id, self.CompanyName)

class Service(models.Model):
    id = models.AutoField(primary_key=True, db_column='ServiceId')
    CompanyName = models.CharField(max_length=255,db_column='CompanyName', null=False)
    ContactPerson = models.CharField(max_length=255,db_column='ContactPerson', null=False)
    ContactPersonType = models.CharField(max_length=255,db_column='ContactPersonType', null=False)
    ServiceTime = models.DateTimeField(db_column='ServiceTime')
    Model = models.CharField(max_length=255, db_column='Model')
    Chassis = models.CharField(max_length=255, db_column='Chassis')
    HRM = models.CharField(max_length=255, db_column='HRM')
    ServiceType = models.CharField(max_length=255, db_column='ServiceType')
    Remark = models.CharField(max_length=255, db_column='Remark')
    Latitude = models.FloatField(default=34.75, db_column='Latitude')
    Longitude = models.FloatField(default=135.5, db_column='Longitude')
    Status = models.CharField(max_length=20, db_column='Status')
    EntryDate = models.DateTimeField(auto_now_add=True,db_column='EntryDate')
    EntryBy = models.ForeignKey(UserManager, db_column='EntryBy', on_delete=models.CASCADE)
    CustomerId = models.ForeignKey(Customer, db_column='CustomerId', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'Service'

    def __str__(self):
        return '{}, {}'.format(self.id, self.CompanyName,
                               self.ContactPerson, self.ContactPersonType,
                               self.ServiceTime, self.Model, self.Chassis,
                               self.Remark, self.Latitude, self.Longitude,
                               self.Status)


class ForwardToSEorSSPE(models.Model):
    id = models.AutoField(primary_key=True, db_column='ApprovedBySSEOrSSPId')
    ServiceId = models.ForeignKey(Service, db_column='ServiceId', on_delete=models.CASCADE)
    AssignedPerson = models.ForeignKey(UserManager, related_name="ForwardToSEorSSPE_AssignedPerson", on_delete=models.CASCADE)
    ApprovedDate = models.DateTimeField(auto_now_add=True, db_column='ApprovedDate')
    Status = models.CharField(max_length=10, db_column='Status')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EntryBy = models.ForeignKey(UserManager, related_name='ForwardToSEorSSPE_EntryBy', on_delete=models.CASCADE)
    IsForwarded = models.CharField(max_length=10, db_column='IsForwarded')

    class Meta:
        managed = False
        db_table = 'ForwardToSEorSSPE'

    def __str__(self):
        return '{}, {}'.format(self.id, self.ServiceId, self.AssignedPerson, self.ApprovedDate, self.Status, self.EntryBy, self.IsForwarded)


class ForwardToEEorSPE(models.Model):
    id = models.AutoField(primary_key=True, db_column='ApprovedByEEorSPEId')
    ServiceId = models.ForeignKey(Service, db_column='ServiceId', on_delete=models.CASCADE)
    AssignedPerson = models.ForeignKey(UserManager, related_name="ForwardToEEorSPE_AssignedPerson", on_delete=models.CASCADE)
    ApprovedDate = models.DateTimeField(auto_now_add=True, db_column='ApprovedDate')
    Status = models.CharField(max_length=10, db_column='Status')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    EntryBy = models.ForeignKey(UserManager, related_name='ForwardToEEorSPE_EntryBy', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'ForwardToEEorSPE'

    def __str__(self):
        return '{}, {}'.format(self.id, self.ServiceId, self.AssigenedPerson, self.ApprovedDate, self.Status,
                               self.EntryBy)

class ServiceAssigned(models.Model):
    id = models.AutoField(primary_key=True, db_column='ServiceAssignedId')
    ServiceId = models.ForeignKey(Service, db_column='ServiceId', on_delete=models.CASCADE)
    To = models.ForeignKey(UserManager, related_name="ServiceAssigned_To", on_delete=models.CASCADE)
    From = models.ForeignKey(UserManager, related_name='ServiceAssigned_From', on_delete=models.CASCADE)
    Status = models.CharField(max_length=10, db_column='Status', default='N')
    EditDate = models.DateTimeField(auto_now_add=True, db_column='EditDate')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    color = models.CharField(max_length=10, db_column='ColorStatus', default='1')
    class Meta:
        managed = False
        db_table = 'ServiceAssigned'

    def __str__(self):
        return '{}, {}'.format(self.id, self.ServiceId, self.To, self.ApprovedDate, self.Status,self.From)


class BoomUser(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    UserId = models.CharField(max_length=50, db_column='UserId')
    UserName = models.CharField(max_length=255, db_column='UserName')
    Password = models.CharField(max_length=100, db_column='Password')
    class Meta:
        managed = False
        db_table = 'UserManager'
    def __str__(self):
        return '{}, {}'.format(self.id, self.UserId, self.Password)



def GetDashboardsByUser(sDate,eDate):
   distinct_user = "SELECT [ServiceId], [CompanyName], [ColorFieldSEorSSPE], [ContactPerson],[ServiceTime],[AssignedSEorSSPEName], [AssignedSEorSSPEWorkStatus],[ColorFieldSEorSSPE], [ServiceColorSEorSSPE],[AssignedEEorSPEName],[AssignedEEorSPEWorkStatus],[ColorFieldEEorSPE],[ServiceColorEEorSPE] FROM vwTaskAssignmentStatus where EntryDate between '"+ sDate+"' and '"+ eDate +"';"
   cur = connections['MotorConstructionEquipment'].cursor()
   cur.execute(distinct_user)
   result = dictfetchall(cur)
   cur.close()
   return result

def dictfetchall(cur):
   dataset = cur.fetchall()
   columns = [col[0] for col in cur.description]
   return [
       dict(zip(columns, row))
       for row in dataset
       ]