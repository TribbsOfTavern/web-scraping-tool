###
#   web-scraping-tool
#   Project 4 given by the AI overlords to learn Python.
#   Written on Stream @ twitch.tv/CodeNameTribbs
#   Requirements:
#   1. Create an app that can scrape informations from a website of your choice.
#   2. Use a web scraping library like BeautifulSoup or Scrapy or Mechanize.
#   3. Define what type of data you want to scrape.
#   4. Implement error handling to gracefully handle situations like failed requests, missing data,
#      or changes in the website's structure.
#   5. Organize the scraped data and display it in a structured format such as a list, table, or CSV file
#   6. Allow the user to specify the number of pages to scrape (if applicacable) and the data to
#       extract (e.g. new headlines from different categories)
#   7. Provide a command line interface that allows the user to input the website URL to specify scraping parameters
#   
#   OPTIONAL: Save the scrapped, formatted data to a file.
#   
#   CHATTER SUGGEST: Dockerize
#   CHATTER SUGGEST: TUI - Terminal User Interface
#   TEST SITE: https://webscraper.io/test-sites
#   TARGET URL: https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops
#-- TODO url validation
#-- TODO request error handling
#-- TODO primary search user input validation
# TODO data parse target data input validation
# TODO data parse get text AND attributes
# TODO handle pagenition
# TODO error handling for missing data
# TODO README.md
# TODO user specify output file and output type
# TODO text ouput dynamic column widths, width of longest value + 2 per column
# TODO move help menu from hardcode to text file, loads in on app start.
# TODO Dockerize

import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def validURL(url:str) -> bool:
    url = url.lower()
    return True if (urlparse(url).scheme == "http" or urlparse(url).scheme == "https") and urlparse(url).netloc else False

def validPrimaryCmd(ins:str) -> bool:
    return True if re.findall("^(\w+) class=\"(\w+ |\w+)+\"$", ins) else False

def validDataSearchCmd(ins:str) -> bool:
    return True if re.findall("^(\w+):(\w+) class=\"(\w+ |\w+)+\"$", ins) else False

def primarySearch(ins:str, soup:BeautifulSoup) -> list:
    pass

def dataSearch(ins:str, primary_results:list):
    pass

def displayHelp():
    text="""
    - URL must be a valid URL
    
    - Primary Container Syntax:
        <element> class="<class name>"
        Ex: div class="card-container"

    -Data Parsing Syntax:
    - You can look for a single item within the primary containers:
        <data title>:<element> class="<class name>"
        Ex: TITLE:h4 class="card-title"
    - Or you can look for multiples of data within the primary container:
        <data title>:<element> class="<class name>" | <data title 2>:<element> class="<class name">
        Ex: TITLE:h4 class="card-title" | DESC:p class="description centered"

    - Information gathered will format into the columns specified by the title of the data collected.
    """
    print(text)

def displayMenu():
    text=""
    text+= f'{"Web Scraper Tool":_^40}\n'
    text+= '\t1.) Start New Search\n'
    text+= '\t2.) View Help\n'
    text+= '\t0.) Exit App\n'
    print(text)
        
def invalidInput(msg:str):
    print(msg)
    input("Press Any Key To Continue...")

def app():
    exit_app = False
    curr_soup = None
    curr_target = None
    curr_target_cmd = None
    curr_data_commands = None

    while not exit_app:
        displayMenu()
        opt = input(">>")
        match opt:
            case "0":
                exit_app = True
            case "1":
                validity = True
                while validity:
                    pass
                    # Ask user for a target url
                    # Ask user for primary target search
                    # Ask user for data parse commands
                    # Ask user for preffered output method
            case "2":
                displayHelp()
            case _:
                invalidInput("Please choose a valid option.")
            
    print("Exiting Webscraper Tool...")

if __name__ == "__main__":
    pass


