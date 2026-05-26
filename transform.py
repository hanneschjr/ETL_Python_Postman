
def transform_airlines(airlines_pages):
    results = []
    airlines = []
    for page in airlines_pages:
        airlines.extend(page.get("airlines"))

    for airline in airlines:
        results.append(            
        {
            "iata": airline.get("iata"),
            "icao": airline.get("icao"),
            "nvls": airline.get("nvls"),
            "name": airline.get("publicName"),
        }
        )
        
    return results

def transform_aircraft_types(aircraft_types_pages):
    results = []
    aircraft_types = []
    for page in aircraft_types_pages:
        aircraft_types.extend(page.get("aircraftTypes"))

    for aircraft_type in aircraft_types:
        results.append(            
        {
            "iataMain": aircraft_type.get("iataMain"),
            "iataSub": aircraft_type.get("iataSub"),
            "description": aircraft_type.get("longDescription"),
        }
        )
        
    return results

def transform_destinations(destinations_pages):
    results = []
    destinations = []
    for page in destinations_pages:
        destinations.extend(page.get("destinations"))

    

    for destination in destinations:
        name = destination.get("publicName")
        if name:
            name = name.get("english")
        results.append(            
        {
            "name": name,
            "country": destination.get("country"),
            "iata": destination.get("iata"),
            "city": destination.get("city"),
        }
        )
        
    return results

def transform_flights_agenda_today(flights_agenda_today_pages):
    results = []
    flights_agenda_today = []
    for page in flights_agenda_today_pages:
        flights_agenda_today.extend(page.get("flights"))

    for flight in flights_agenda_today:
        aircraftType = flight.get("aircraftTypes")
        aircraftType_iataMain = None
        aircraftType_iataSub = None
        if aircraftType:
            aircraftType_iataMain = aircraftType.get("iataMain")
            aircraftType_iataSub = aircraftType.get("iataSub")
        
        route = None
        originIata = None
        visa = None
        flight_route = flight.get("route")
        if flight_route:
            destinations = flight_route.get("destinations")
            eu = flight_route.get("eu")
            visa = flight_route.get("visa")
            if destinations:
                route = ",".join(destinations):
        
        codeshares = None
        flight_codeshares = flight.get("codeshares")
        if flight_codeshares:
            flight_codeshares = flight_codeshares.get("codeshares")
            if flight_codeshares:
                codeshares = ",".join(flight_codeshares)
        
        flight_states = None
        public_flight_states = flight.get("publicFlightStates")
        if public_flight_states:
            flight_states = public_flight_states.get("flightStates")
            if flight_states:
                flight_states = ",".join(flight_states)

        atributos = {
            "aircraftType_iataMain": aircraftType_iataMain,
            "aircraftType_iataSub": aircraftType_iataSub,
            "route": route,
            "codeshares": codeshares,
            "flight_states": flight_states,
            "eu": eu,
            "visa": visa,
        }
        atributos.update(
            atributos_for_dict(
                flight, 
                [
                    "flightDirection", 
                    "flightName",
                    "flightNumber",
                    "gate",
                    "pier",
                    "id",
                    "isOperationalFlight",
                    "mainFlight",
                    "prefixIATA",
                    "prefixICAO",
                    "airlineCode",
                    "aircraftRegistration",
                    "serviceType",
                    "terminal",
                ]
            )
        )

        results.append(            
        {
            "flightId": flight.get("flightId"),
            "scheduleDate": flight.get("scheduleDate"),
            "airlineIata": flight.get("airlineIata"),
            "flightNumber": flight.get("flightNumber"),
            "originIata": flight.get("originIata"),
            "destinationIata": flight.get("destinationIata"),
            "aircraftTypeIataMain": aircraftType_iataMain,
            "aircraftTypeIataSub": aircraftType_iataSub,
            "route": route,
            "visa": visa,
            "codeshares": codeshares,
        }
        )
        
    return results