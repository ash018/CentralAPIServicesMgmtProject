from rest_framework import routers
from .views import UploadToS3

from django.conf.urls import url, include

router = routers.DefaultRouter()
router.register(r'UploadToS3', UploadToS3, base_name='UploadToS3')

# Wire up our API with our urls
urlpatterns = [
    url(r'^', include(router.urls)),
]