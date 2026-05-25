from decouple import config
from requests import request
from constants import BASE_URL
import re
import logging
import os
from pathlib import Path
import time
from datetime import datetime, timedelta
import pytz

#
# Configurnado o arquivo de log para verificar a lista de links #
#
logging.basicConfig(filename=os.path.join(str(Path.cwd()), "aeroporto.log"), # caminho do arquivo
                    format="%(asctime)s %(message)s", # fomato, conforme documentação da biblioteca
                    filemode="w") # modo de escrita

logger = logging.getLogger(__name__) # variável usada para imprimir dentro do arquivo .log.
                                    # No caso, __name__ é o nome do módulo, ou seja, extract.py.
                                    # Assim, no arquivo de log, aparecerá o nome do módulo que fez a requisição.
                                    # Cada logger é independente, ou seja, cada módulo pode ter um logger diferente, com configurações diferentes.
                                    # Por que isso é melhor? Porque você descobre exatamente qual módulo fez a requisição,
                                    # e pode configurar cada módulo para ter um nível de log diferente, por exemplo, um módulo pode ter nível de log DEBUG,
                                    #  e outro módulo pode ter nível de log INFO.

logger.setLevel(logging.DEBUG)  # nível de DEBUG inclui informações sobre pacote requests


def get_endpoint(endpoint, endpoint_id=None, params=None):

    headers = {
        "Accept": "application/json",
        "app_id": config("PUBLIC_KEY"),
        "app_key": config("SECRET_KEY"),
        "ResourceVersion": "v4",
    }

    url = f"{BASE_URL}{endpoint}"
    if endpoint_id:
        url += f"/{endpoint_id}"  
    
    result_list = []

    result_get = request("GET", url, headers=headers, params=params)
    result_get.raise_for_status()
    result_list.append(result_get.json())

    number_pages = process_headers_number_of_pages(result_get.headers)

    # link_next_page = process_headers_next_page(result_get.headers)

    while link_next_page:= process_headers_next_page(result_get.headers):
        time.sleep(0.5)
        logger.info(f"Págins: {number_pages} link: {link_next_page}")
        result_get = request("GET", link_next_page, headers=headers)
        result_get.raise_for_status()
        result_list.append(result_get.json())
    # import ipdb; ipdb.set_trace()
    return result_list

def process_headers_number_of_pages(headers):
    headers_link = headers.get("Link", "")

    if not headers_link:
        return '0'
    
    link_parts = headers_link.split(",")

    pattern = r'.*page=([0-9]+).*'

    for link_part in link_parts:
        if 'rel="last"' in link_part:
            number = link_part.split(";")[0]
            number = re.search(pattern, number)
            # import ipdb; ipdb.set_trace()
            return number.groups()[0]
    return '0'
        
def process_headers_next_page(headers):
    headers_link = headers.get("Link", "")

    if not headers_link:
        return None
    
    link_parts = headers_link.split(",")

    pattern = r'<(.*)>'

    for link_part in link_parts:
        if 'rel="next"' in link_part:
            next = link_part.split(";")[0]
            next = re.search(pattern, next)
            # import ipdb; ipdb.set_trace()
            return next.groups()[0]

def get_flights_agenda_today():
    return get_endpoint("flights")

def get_flights_agenda_yesterday():
    now = pytz.timezone("Europe/Amsterdam").localize(datetime.now())
    yesterday = now - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    params = {"scheduleDate": yesterday_str}
    return get_endpoint("flights", params=params)

def get_flights_for_id(flight_id):
    return get_endpoint(endpoint="flights", endpoint_id=flight_id)

def get_airlines():
    return get_endpoint(endpoint="airlines")

def get_airlines_for_iata_icao(iata_icao):
    return get_endpoint(endpoint="airlines", endpoint_id=iata_icao)

def get_arcraft_types():
    return get_endpoint(endpoint="aircrafttypes")

def get_destinations():
    return get_endpoint(endpoint="destinations")

def get_destinations_for_iata(iata):
    return get_endpoint(endpoint="destinations", endpoint_id=iata)


if __name__ == "__main__":
   print(get_destinations_for_iata("AAA"))

