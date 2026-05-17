from decouple import config
from requests import request
from constants import BASE_URL
import re



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

    result_get = request("GET", url, headers=headers, params=params)

    number_pages = process_headers_number_of_pages(result_get.headers)

    import ipdb; ipdb.set_trace()



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


if __name__ == "__main__":
   print(get_endpoint("flights"))
