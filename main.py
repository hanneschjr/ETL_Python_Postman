from extract import get_airlines
from save import save
from transform import transform_airlines


def main_etl():
    # Extract
    airlines_pages = get_airlines()

    # Transform
    airlines = transform_airlines(airlines_pages)

    # Load
    save(
        "./",
        [
            airlines,    
        ],
        [
            "airlines",
        ]
    )






if __name__ == "__main__":
   main_etl()
