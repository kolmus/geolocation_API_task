from django.db.models import fields
from rest_framework import serializers
from .models import Localization


class LocalizationSerializer(serializers.Serializer):
    ipv4 = serializers.CharField(max_length=16)
    domain = serializers.CharField(ma_length=128)
