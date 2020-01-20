from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^PharmaCampaign/', include('PharmaCampaignApp.urls')),
	#url(r'^MotorConstructionEuip/', include('ConstructionEquipmentApp.urls')),
	url(r'^MotorConstructionEquipment/dataprovider/', include('ConstructionEquipmentApp.urls')),
	url(r'^YamahaRegistrationAPI/Dataprovider/', include('YamahaRegistrationAPI.urls')),
	url(r'^PrescriptionUploader/Uploader/', include('RxCampS3Uploader.urls')),
	url(r'^yamahabooking/dataprovider/', include('YamahaBookingApp.urls')),
    url(r'^genericservice/api/v0/', include('GenericServiceRESTApp.urls')),
] 
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

