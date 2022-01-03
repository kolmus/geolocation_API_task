from geo_api_app.models import Location
import pytest

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