from rest_framework import routers
from .views import *
from .models import *

from django.conf.urls import url, include

router = routers.DefaultRouter()
router.register(r'Level4CampaignForApproval', Level4CampaignForApproval)
router.register(r'Level5CampaignForApproval', Level5CampaignForApproval)
router.register(r'Level6CampaignForApproval', Level6CampaignForApproval)
router.register(r'Level7CampaignForApproval', Level7CampaignForApproval)

# router.register(r'BaseUrl', APIRootView)


# Wire up our API with our urls
urlpatterns = [
    url(r'^', include(router.urls)),
]