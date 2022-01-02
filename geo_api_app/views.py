from django.shortcuts import render
from django.http import Http404
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

from validators import domain, ipv4
from validators.utils import ValidationFailure
from socket import gethostbyname

from .models import Location
from .serializers import AddLocationSerializer, GetLocationSerializer
# Create your views here.


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
        
