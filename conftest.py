from geo_api_app.tests.utils import create_location
import pytest
from socket import gethostbyname


@pytest.fixture
def location():
    ip_adresses = [
        "87.207.208.222",
        "51.83.129.136",
        gethostbyname('sofomo.com'),
    ]
    for i in ip_adresses:
        new_location = create_location(ip=i)
    return new_location
