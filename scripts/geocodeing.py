from mapbox import Geocoder
from typing import Tuple

def get_coords(address: str) -> Tuple[float, float]:
    # t
    MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiYWFyYXRoYSIsImEiOiJjbGw5eWZ6anExaDJtM2VtenpuZHJ1c2FuIn0.TOfFT2m_2oDuHFgjEFYiYg'
    geocoder= Geocoder(access_token=MAPBOX_ACCESS_TOKEN)
    response = geocoder.forward(address)

    coords = str(response.json()['features'][0]['center'])
    coords = coords.replace(']', '')
    coords = coords.replace('[', '')
    latitude = coords.split()[1][0:-2]
    longitude = coords.split()[0][0:-2]
    float(latitude)
    float(longitude)
    return latitude, longitude
