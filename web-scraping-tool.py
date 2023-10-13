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
    """
    Given a str will check if it is a valid url entry and return a bool.
    This does not check if the url is a valid landing site, only syntax.
    
    params:
        url : str - String input to check for valid url syntax
    return:
        bool - True if url string was valid syntax otherwise False
    """
    parsed = urlparse(url)
    if (parsed.scheme == "http" or parsed.scheme == "https") and parsed.netloc:
        return True
    else:
        return False

def getPrimaryResults(ins:str, soup:BeautifulSoup) -> list:
    """
    Parse primary search command and return resulting data from search.
    
    params:
        ins : str - String input should be a primary target.
        soup : bs4.BeautifulSoup - BeautifulSoup class for primary target.
    return:
        list[bs4.element.Tag] - Returns list of class bs4.element.Tag
    """
    if not validPrimaryCmd(ins): raise Exception("Invalid primary target cmd syntax.")
    ins = ins.split(' ', 1)
    ins[1] = ins[1].replace('"', '').strip().split('=')
    return soup.find_all(ins[0], class_=ins[1][1])

def validPrimaryCmd(cmd:str) -> bool:
    """
    Check if the primary command is a valid syntax.
    This does not check if its proper data to fetch.
        
    params:
        cmd : str - String input from the user that should be primary data search command.
    return:
        bool - True if correct syntax otherwise False
    """
    pattern = "^(\w)+:(\w)+ class=\"(\w|\w )+\"$"
    result = re.findall(pattern, cmd)
    if result:
        return True
    else:
        return False

def getDataResults(ins:str, pres:list) -> list:
    """
    Parse data search parameters and return resuling data.
    
    params:
        ins : str - String input should be a series of targetted tags with valid application
            syntax.
        pres: list[bs4.element.Tag] - List of bs4.element.Tag class objects.
    return:    
        list[dict] - Returns a list of parsed data, each dict containing key of the command title,
        and value containing the parsed data.
    """
    ins = ins.split('|')
    ins = [x.replace('"', '').strip() for x in ins]
    
    targets = []
    for i, search in enumerate(ins):
        ins[i] = search.split(' ', 1)
        targets.append(
            {'name': ins[i][0].split(':')[0].strip(),
             'element': ins[i][0].split(':')[1].strip(),
             'class': ins[i][1].split('=')[1]})
    
    results = []
    for each in pres:
        result = {}
        for t in targets:
            result[t['name']] = None
        for target in targets:
            result[target['name']] = each.find(target['element'], class_=target['class']).text
        results.append(result)
    
    return results

def formatData(data:list[dict], width:int=20) -> str:
    """
    Format data into text columns
    
    params:
        data : list[dict] - List of dicts.
        width : int - default 20 - width columns should be formatted to.
    returns:
        str - Contains the formatted text string of data.
    """
    text = ""
    for k in data[0].keys():
        text+=f"{k:<{width}}"
    text += "\n"
    for each in data:
        for k, v in each.items():
            text += f"{v:<{width}}"
        text += "\n"

    return text

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
    """
    Display the menu of options for the applications
    """
    text=""
    text+= f'{"Web Scraper Tool":_^40}\n'
    text+= '\t1.) Start New Search\n'
    text+= '\t2.) View Help\n'
    text+= '\t0.) Exit App\n'
    print(text)

def newSearch():
    """
    Perform a new web scrape action.
    User will be required to provide a target url.
    User will be required to provide a primary target syntax.
    User will be required to provide a parsing syntax.
    
    Successful output will result in a formatted string output to console.
    """
    target_url = input("Enter full target url: ")
    try:
        if not validURL(target_url): raise Exception("Invalid URL syntax. HTTP or HTTPS must be included in the target URL.")
        page = requests.get(target_url)
        if page.status_code != "200": raise Exception("Failed to get response. Response code: ", page.status_code)
    except Exception as e:
        print("ERROR: ", e)
        exit()
    soup = BeautifulSoup(page.content, "html.parser")
    
    primary_input = input("Enter primary container target: ")
    primary_results = getPrimaryResults(primary_input, soup)    
        
    data_input = input("Enter target data: ")
    data_results = getDataResults(data_input, primary_results)

    print(formatData(data_results))

def app():
    """
    Main App Function for Web Scraper Tool.
    """
    exit_app = False
    while not exit_app:
        displayMenu()
        opt = input(">> ")
        match opt:
            case "0":
                exit_app = True
            case "1":
                newSearch()
            case "2":
                displayHelp()
            case _:
                pass
            
    print("Exiting Web Scraper Tool...")
    
if __name__ == "__main__":
    app()