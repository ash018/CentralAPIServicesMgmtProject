from rest_framework import routers
from .views import *
from .models import UserInfo

from django.conf.urls import url, include

router = routers.DefaultRouter()
router.register(r'login', LoginViewSet)
router.register(r'manageservice', ServiceDetailsViewSet)
router.register(r'getuserservice', GetUserServiceViewSet)
router.register(r'getservicevsachievement', GetTargetVsAchievement)

# router.register(r'BaseUrl', APIRootView)

# Wire up our API with our urls
urlpatterns = [
    url(r'^', include(router.urls)),
]