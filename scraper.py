import argparse
import logging
import requests
import json
import os
from time import gmtime, strftime

# Define logger format
LOGGER_FORMAT = '%(levelname)s:%(asctime)s:%(name)s:%(message)s'
TIME = strftime("%Y%m%d_%H%M%S", gmtime())

# Define logger and stream handler - no file handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(LOGGER_FORMAT)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def airbnb_scraper(link):
    """Scraper for AirBnB website

    :param link: Link for property of interest
    :return: File with the property name, property type, number
        of bedrooms, number of bathrooms and list of amenities.
    """

    return {
        'property_name' : property_name,
        'property_type' : property_type,
        'n_bedrooms' : n_bedrooms,
        'n_bathrooms' : n_bathrooms,
        'amenities' : amenities
    }


def link_handler(links_file, out_type):

    file_type = out_type.lower()

    # Import file at location links_file


    # Open save file with name airbnb_properties_$time.out_type
    if file_type == 'csv':
        # Save files in csv file
        pass

    elif file_type == 'json':
        # Save files in json file
        pass

    else:
        raise ValueError('Out-type {} not found'.format(file_type))



    # Iterate through links and save values

    for idx, property_link in enumerate(links):

        # Get property details using the requested scraper
        # For other website types introduce another scraper.
        # Example - bookingdotcom_scraper(property_link)
        property_details = airbnb_scraper(property_link)

        # Save values


    # Close save file


    # Close links file



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--links-file',
                        required=True,
                        type=str,
                        help='Local dir with the links for the properties in .txt format')

    parser.add_argument('--out-type',
                        default='csv',
                        type=str,
                        help='Output file type for scraping results')

    parse_args, unknown = parser.parse_known_args()

    # If unknown arguments found, warn them on the console
    logger.warning('Unknown arguments: {}'.format(unknown))
    airbnb_scraper(**parse_args.__dict__)