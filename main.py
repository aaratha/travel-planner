#!/usr/bin/env python3
from amadeus import Client, ResponseError
from scripts import get_coords


amadeus = Client(
    client_id='FL5z5GTmtjkPXFBFGyM85nTXSyRgAZkd',
    client_secret='xTbasGMlel9dpscA'
)


INIT_PASSENGERS = {"Aseem": "62 earl st, toronto, ontario, canada",
              "Neel": "7512 glenriddle rd, bethesda, maryland, usa"}
DESTINATIONS = ["Chicago", "Paris"]
MAX_AIRPORT_DISTANCE = 90 #km

class Passenger:

    def __init__(
        self,
        name: str,
        address: str,
        coords: tuple[float, float] = None,
        airports: list = None
    ):
        self.name = name
        self.address = address
        self.coords = coords if coords is not None else (0.0, 0.0)  # Initialize to (0.0, 0.0) or user-provided
        self.airports = airports if airports is not None else []

    def __repr__(self):
        return (f"Passenger(name={self.name}, address={self.address}, "
                f"coords={self.coords}, airports={self.airports})")


def find_offers(origin, destination, date, adult_n):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=date,
            adults=adult_n)
        print(response.data)
    except ResponseError as error:
        print(error)


def get_coordinates(
    # uses address to find coordinates and add to passengers
        passengers: list[Passenger]) -> None:
    for passenger in passengers:
        try:
            passenger.coords = get_coords(passenger.address)
        except ResponseError as error:
            print(f"Error finding coordiantes for {passenger.name}: {error}")



def get_airports(passengers: list[Passenger]) -> None:
    # Finds airports near the passenger's coordinates within MAX_AIRPORT_DISTANCE.
    for passenger in passengers:
        try:
            response = amadeus.reference_data.locations.airports.get(
                latitude=passenger.coords[0],
                longitude=passenger.coords[1],
                radius=MAX_AIRPORT_DISTANCE  # Radius in miles
            )

            # Add airports to passenger's list
            passenger.airports = [airport['iataCode'] for airport in response.data]

        except ResponseError as error:
            print(f"Error finding airports for {passenger.name}: {error}")



def main():
    # main process
    passengers = [Passenger("Aseem",
                            "2600 Benjamin Franklin Pkwy, philadelphia"
                            ),
                  Passenger("Neel"
                            , "7512 glenriddle rd., bethesda, maryland, usa"
                            ),
                  Passenger("Sven", "san francisco")
                  ]
    # find_offers('MAD', 'ATH', '2024-11-01', 1)
    get_coordinates(passengers)
    get_airports(passengers)
    print(passengers)


main()
