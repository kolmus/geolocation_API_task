from django.db import models

# Create your models here.

class Location (models.Model):
    ipv4 = models.CharField(max_length=16, verbose_name='IPv4 adress or domain')
    continent = models.CharField(max_length=32, verbose_name='Continent name')
    country = models.CharField(max_length=64, verbose_name='Country name')
    region = models.CharField(max_length=64, verbose_name='Region')
    city = models.CharField(max_length=64, verbose_name='City')
    zip_code = models.CharField(max_length=6, verbose_name='Zip code')
    lattitude = models.CharField(max_length=32, verbose_name='Lattitude')
    longitude = models.CharField(max_length=32, verbose_name='Longitude')
    add_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ip  => {self.ipv4}'
