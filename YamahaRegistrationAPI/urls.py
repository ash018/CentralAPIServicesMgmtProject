from rest_framework import routers
from .views import *

from django.conf.urls import url, include

router = routers.DefaultRouter()
router.register(r'ValidateUser', ValidateUser)
router.register(r'GetRegistrationStatus', GetRegistrationStatus)

# router.register(r'BaseUrl', APIRootView)


# Wire up our API with our urls
urlpatterns = [
    url(r'^', include(router.urls)),
]