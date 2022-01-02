from rest_framework import serializers

from geo_api_app.models import Location


class AddLocationSerializer(serializers.Serializer):
    ipv4 = serializers.CharField(max_length=16, null=True)
    domain = serializers.CharField(ma_length=128, null=True)


class GetLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'ipv4', 'continent', 'country', 'region', 'city', 'zip_code', 'lattitude', 'longitude', 'add_datetime')
        
