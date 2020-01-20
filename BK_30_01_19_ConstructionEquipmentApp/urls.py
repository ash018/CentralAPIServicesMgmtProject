from rest_framework import routers
from .views import LoginCheck, EngAndSS, MecAndSpo, SaveService, PendingSaveService, ForwardToMecnSpo, JobDoneByMecnSpo
from .models import Role,UserManager

from django.conf.urls import url, include

router = routers.DefaultRouter()
#router.register(r'ImageExtractAPI', ImageViewSet) , BaseAPICallURL ,BaseUrlConfig
router.register(r'logincheck', LoginCheck)
router.register(r'allengnssuser', EngAndSS)
router.register(r'allmecnspouser', MecAndSpo)
router.register(r'saveservice', SaveService)
router.register(r'pendingservice', PendingSaveService)
router.register(r'forwardtomecnspo', ForwardToMecnSpo)
router.register(r'jobdonebymecnspo', JobDoneByMecnSpo)
#router.register(r'servicedetail', PendingSaveService)
#router.register(r'BaseUrl', BaseAPICallURL)
#router.register(r'BaseUrl', APIRootView)
# Wire up our API with our urls
urlpatterns = [
    url(r'^', include(router.urls)),
]