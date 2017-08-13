import os
import logging
import argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from time import gmtime, strftime

# Define logger format
LOGGER_FORMAT = '%(levelname)s:%(asctime)s:%(name)s:%(message)s'
TIME = strftime("%m%d_%H%M", gmtime())

# Define logger and stream handler - no file handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(LOGGER_FORMAT)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


# Function to scrape from airbnb property link.
# Returns: Property name and type, room type, number of bedrooms
#   number of bathrooms and amenities
def airbnb_scraper(response_source):
    """Scraper for AirBnB website

    :param response_source: Source from browser
    :return: File with the property name, property type, number
        of bedrooms, number of bathrooms and list of amenities.
    """

    html_soup = BeautifulSoup(response_source, "html.parser")
    page_description = html_soup.findAll("div", {"class": "room__dls"})[0]
    room_details = page_description.findAll("div", {"id": "details"})[0]

    # Get property name
    property_name = page_description.find("div", {"itemprop": "name"}).text

    # Get basic details
    property_type = room_details.find(text="Property type:").parent.find("strong").text
    room_type = room_details.find(text="Room type:").parent.find("strong").text
    n_bedrooms = room_details.find(text="Bedrooms:").parent.find("strong").text
    n_bathrooms = room_details.find(text="Bathrooms:").parent.find("strong").text

    # Get amenities list
    amenities_section = room_details.findAll("div", {"class": "amenities"})[0]
    all_amenities = amenities_section.findAll("div", {"class": "expandable-content expandable-content-full"})[0]
    amenities = '|'.join([element.text for element in all_amenities.findAll("strong")])

    return {
        'property_name': property_name,
        'property_type': property_type,
        'room_type': room_type,
        'n_bedrooms': n_bedrooms,
        'n_bathrooms': n_bathrooms,
        'amenities': amenities
    }


# Function to handle the links being processed.
# These are loaded from the links file data obtained from the
# scraper being used and saved in file.
def links_handler(links_file, out_type):
    """ Links handler

    Loads property links from links_file and saves the results of the
    scaper in a results file
    """
    file_type = out_type.lower()
    save_file_headers = 'Property Name, Property Type, Room Type, Number of Bedrooms, Number of Bathrooms, Amenities\n'

    # Open save file with name airbnb_properties_$time.out_type
    if file_type == 'csv':
        save_file = open('results_{}.csv'.format(TIME), 'w')
        save_file.write(save_file_headers)
    else:
        raise ValueError('Out-type {} not found'.format(file_type))

    # Open browser for javascript rendering
    browser = webdriver.PhantomJS(service_log_path=os.path.devnull)

    # Iterate through links and save values
    with open(links_file) as file:
        for property_link in file:
            browser.get(property_link)
            # Get property details using the requested scraper
            # For other website types introduce another scraper.
            # Example - bookingdotcom_scraper(property_link)
            property_details = airbnb_scraper(browser.page_source)
            logger.info('Property details loaded')

            #for item_name, item_value in property_details.items():
            #    print('{}:\t{}'.format(item_name, item_value))

            # Save values
            property_details_values = list(property_details.values())
            if file_type == 'csv':
                save_file.write(','.join(property_details_values) + '\n')
            logger.info('Property details saved')

    # Close browser
    browser.quit()

    # Close save file
    save_file.close()


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
    links_handler(**parse_args.__dict__)