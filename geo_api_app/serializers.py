from rest_framework import serializers

from geo_api_app.models import Location


# class AddDeleteLocationSerializer(serializers.Serializer):
#     ip_domain = serializers.CharField(max_length=64, null=True)


class GetLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'ipv4', 'continent', 'country', 'region', 'city', 'zip_code', 'lattitude', 'longitude', 'add_datetime')
