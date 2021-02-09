from geopy.geocoders import Nominatim
import csv

geolocator = Nominatim(user_agent="matepa12@gmail.com")

with open('data.csv', 'r', newline='\n') as data:
    reader = csv.reader(data)
    rows = list(reader)
    regions = {row[1] for row in rows}
    count = 0
    with open('geoloc.csv', 'a') as geoloc:
        for region in regions:
            try:
                location = geolocator.geocode(region + ',' + 'małopolskie', country_codes='pl', timeout=30)
                print(region + ', ' + location.address + ', ' + str(location.latitude) + ', ' + str(location.longitude),
                      file=geoloc)
            except AttributeError:
                try:
                    location = geolocator.geocode(region + ',' + 'śląskie', country_codes='pl', timeout=30)
                    print(region + ', ' + location.address + ', ' + str(location.latitude) + ', ' + str(location.longitude),
                          file=geoloc)
                except AttributeError:
                    pass
