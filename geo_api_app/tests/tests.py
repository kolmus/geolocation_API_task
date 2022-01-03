from django.db.models import fields
from geo_api_app.models import Location
import pytest
from socket import gethostbyname


@pytest.mark.django_db
def test_show_location(client, location):
    ip = Location.objects.all()[0].ipv4
    response = client.get(f'/location/{ip}/', format="json")
    assert response.status_code == 200
    for field in (
        'ipv4', 
        'continent', 
        'country', 
        'region', 
        'city', 
        'zip_code', 
        'lattitude', 
        'longitude', 
        'add_datetime'
    ):
        assert field in response.data

@pytest.mark.django_db
def test_delete_location(client, location):
    loc_obj = Location.objects.first()
    loc_id = loc_obj.id
    response = client.delete(f'/location/del/{loc_obj.ipv4}/', {}, format='json')
    assert response.status_code == 204
    locations_ids = [loc.id for loc in Location.objects.all()]
    assert loc_id not in  locations_ids

@pytest.mark.django_db
def test_add_location(client, location):
    localization_count = Location.objects.count()
    ip_to_test = gethostbyname('google.com')
    response = client.post(f'/location/add/{ip_to_test}/', {}, format='json')
    
    assert response.status_code == 201
    assert Location.objects.count() == localization_count + 1
