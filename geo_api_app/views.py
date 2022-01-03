from django.shortcuts import render
from django.http import Http404
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

from validators import domain, ipv4
from validators.utils import ValidationFailure
from socket import gethostbyname
import requests
# import json

from .models import Location
from .serializers import GetLocationSerializer

def validate_ip_domain(ip_domain):
    """Checks validatiof of IP adress or Domain, 

    Args:
        ip_domain (str): IPv4 or Domain name, No objects with this IP adress in database 

    Raises:
        Http404: Invalid IP or domain name

    Returns:
        valid_ip (str): valid IPv4 => from argument or got by domain name
    """        
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
    return str(valid_ip)
    

class LocationView(APIView):
    def get(self, request, ip_domain, format=None):
        """View to get data about exact IP or Domain from database. 

        Args:
            ip_domain (str): IPv4 or domain name

        Returns:
            Data from  Database about exact ip
        """        
        valid_ip = validate_ip_domain(ip_domain=ip_domain)
        try:                                # check if exists
            loc_object = Location.objects.get(ipv4=valid_ip)
        except Location.DoesNotExist:
            raise Http404
        serializer = GetLocationSerializer(loc_object, context={'request': request})
        return Response(serializer.data)
    
    
class DeleteLocationView(APIView):
    def delete(self, request, ip_domain, format=None):
        """Delete objects from database

        Args:
            ip_domain (str): IPv4 or domain name

        Returns:
            HTTP_204: Object deleted
        """        
        valid_ip = validate_ip_domain(ip_domain=ip_domain)
        try:                                # check if exists
            loc_object = Location.objects.get(ipv4=valid_ip)
        except Location.DoesNotExist:
            raise Http404
        loc_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class AddLocationView(APIView):
    def post(self, request, ip_domain, format=None):
        """POST method checks validation of IP or Domain, turns Domein into IPv4 and fetch to external API on https://ipstack.com for data to save new object of Location Model

        Args:
            ip_domain (str): IPv4 or domain name

        Raises:
            Http404: invalid IP or invalid domain

        Returns:
            HTTP_201: Created
            HTTP_429: Over 100 requests in this month to ipstack 
            HTTP_504: Timeout to ipstack API
            HTTP_404: Other Problems
        """        
        print("##################################  w środku, działa")
        valid_ip = validate_ip_domain(ip_domain=ip_domain)
        from geolocation_api.local_settings import API_KEY
        try:
            response = requests.get(f'http://api.ipstack.com/{valid_ip}?access_key={API_KEY}')
            response.raise_for_status()
            if response.status_code == 200:
                loc_object = Location()
                loc_object.ipv4 = valid_ip
                loc_object.continent = response.json()['continent_name']
                loc_object.country = response.json()['country_name']
                loc_object.region = response.json()['California']
                loc_object.city = response.json()['city']
                loc_object.zip_code = response.json()['90012']
                loc_object.lattitude = response.json()['latitude']
                loc_object.longitude = response.json()['longitude']
                loc_object.save()
                return Response(status=status.HTTP_201_CREATED)
            if response.status_code == 104:
                return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)
        except requests.exceptions.HTTPError as error:
            print(error)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except requests.Timeout as error:
            print(error)
            return Response(status=status.HTTP_504_GATEWAY_TIMEOUT)


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

# to check https://ipapi.co/  https://ipapi.co/json