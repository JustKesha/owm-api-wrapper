class Location():
    def __init__(self, type:str, name:str, region:str, country:str, country_code:str, lat:float, lon:float) -> None:
        self.type = type
        self.name = name
        self.region = region
        self.country = country
        self.country_code = country_code

        self.lat = lat
        self.lon = lon

    def get_google_maps_url(self) -> str:
        return f'https://maps.google.com/?q={self.lat},{self.lon}'

    def get_address_str(
            self,
            full:bool=False,
            include_type:bool=False,
            ) -> str:
        
        elements = []

        if not include_type:
            elements.append(self.name)
        else:
            elements.append(f'{self.name} {self.type}')

        if self.region and full:
            elements.append(self.region)
        
        elements.append(self.country)

        return ', '.join(elements)

    # NOTE Atm only used in a test discord command
    def get_str(self):
        return f'{" ".join([str(self.lat), str(self.lon)])} {self.get_address_str(full=True,include_type=True)} {self.country_code}'

def format_raw_location_data(raw_location:dict) -> Location:
    address_type = raw_location['addresstype']
    address = raw_location['address']

    return Location(
        type=address_type,

        name=address[address_type],
        region=address['state'] if 'state' in address else None,
        country=address['country'],
        
        country_code=address['country_code'],

        lat=raw_location['lat'],
        lon=raw_location['lon'],
    )

def format_raw_locations_data(raw_locations:list) -> list:
    return list(map(lambda location: format_raw_location_data(location), raw_locations))
