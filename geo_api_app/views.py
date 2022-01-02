from django.shortcuts import render
from django.http import Http404
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

from validators import domain, ipv4
from validators.utils import ValidationFailure
from socket import gethostbyname
import requests
import json

from .models import Location
from .serializers import AddLocationSerializer, GetLocationSerializer



class LokalizationView(APIView):
    def get_object(self, ip_domain):
        try:                                # check ip
            valid_ip = ipv4(ip_domain)
            valid_ip = ip_domain
        except ValidationFailure:
            try:                            # check doimain if ip is invalid
                valid_domain = domain(ip_domain)
            except ValidationFailure:
                raise Http404
            try:                            # if domain is valid get ip
                valid_ip = gethostbyname(ip_domain)
            except:
                raise Http404
        try:                                # check if exists
            return Location.objects.get(ipv4=valid_ip)
        except Location.DoesNotExist:
            raise Http404
    
    def get(self, request, ip_domain, format=None):
        loc_object = self.get_object(ip_domain=ip_domain)
        serializer = GetLocationSerializer(loc_object, context={'request': request})
        return Response(serializer.data)
    
    def delete(self, request, ip_domain, format=None):
        loc_object = self.get_object(ip_domain=ip_domain)
        loc_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def post(self, request, ip_domain, format=None):
        loc_object = Location()
        try:                                # check ip
            valid_ip = ipv4(ip_domain)
            valid_ip = ip_domain
        except ValidationFailure:
            try:                            # check doimain if ip is invalid
                valid_domain = domain(ip_domain)
            except ValidationFailure:
                raise Http404
            try:                            # if domain is valid get ip
                valid_ip = gethostbyname(ip_domain)
            except:
                raise Http404
    ##### Import here #####
        


"""Exampe of response {
    "ip": "134.201.250.155", 
    "type": "ipv4", 
    "continent_code": "NA", 
    "continent_name": "North America", 
    "country_code": "US", 
    "country_name": "United States", 
    "region_code": "CA", 
    "region_name": "California",
    "city": "Los Angeles",
    "zip": "90012",
    "latitude": 34.0655517578125,
    "longitude": -118.24053955078125,
    "location": {
        "geoname_id": 5368361,
        "capital": "Washington D.C.",
        "languages": [{
            "code": "en",
            "name": "English",
            "native": "English"
        }],
        "country_flag": "https://assets.ipstack.com/flags/us.svg",
        "country_flag_emoji": "\ud83c\uddfa\ud83c\uddf8",
        "country_flag_emoji_unicode": "U+1F1FA U+1F1F8",
        "calling_code": "1",
        "is_eu": false
    }
}

"""