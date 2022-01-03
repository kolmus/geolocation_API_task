from geo_api_app.models import Location

def create_location(ip):
    """Creates new object in database with fake data

    Args:
        ip (str): IPv4 - exemple

    Returns:
        obj: New object of Location model
    """   
    location = Location()
    location.ipv4 = str(ip)
    location.continent = f'Europe'
    location.country = f'Poland'
    location.region = f'Mazowieckie'
    location.city = f'Warszawa'
    location.zip_code = f'{ip[:1]}356'
    location.lattitude = f'60.0000'
    location.longitude = f'-70.000'
    location.save()
    return location