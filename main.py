from extract import get_airlines, get_destinations, get_arcraft_types, get_flights_agenda_today
from load import load
from transform import transform_aircraft_types, transform_airlines, transform_destinations, transform_flights_agenda_today


def main_etl():
    # Extract
    airlines_pages = get_airlines()
    # aircraft_types_pages = get_arcraft_types()
    # destinations_pages = get_destinations()
    # flights_agenda_today_pages = get_flights_agenda_today()

    # Transform
    airlines = transform_airlines(airlines_pages)
    # aircraft_types = transform_aircraft_types(aircraft_types_pages)
    # destinations = transform_destinations(destinations_pages)
    # flights_agenda_today = transform_flights_agenda_today(flights_agenda_today_pages)

    # Load
    load(
        "./",
        [
            airlines,
            # aircraft_types,
            # destinations,
            # flights_agenda_today,
        ],
        [
            "airlines",
            # "aircraft_types",
            # "destinations",
            # "flights",
        ]
    )






if __name__ == "__main__":
   main_etl()
