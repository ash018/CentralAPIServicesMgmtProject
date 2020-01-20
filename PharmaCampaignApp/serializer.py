from rest_framework import serializers

from .models import *



class Level4CampaignApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('CampaignId', 'CampaignName')

class Level5CampaignApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('CampaignId', 'CampaignName')

class Level6CampaignApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('CampaignId', 'CampaignName')

class Level7CampaignApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('CampaignId', 'CampaignName')