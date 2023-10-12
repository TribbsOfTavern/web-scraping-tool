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
#   TARGET SITE: https://webscraper.io/test-sites

# TODO url validation
# TODO request error handling
# TODO primary search user input validation
# TODO data parse user input validation
# TODO data parse get text AND attributes
# TODO handle pagenition
# TODO error handline for missing data
# TODO README.md
# TODO user specify output file and output type
# TODO text ouput dynamic column widths, width of longest value + 2 per column
# TODO move help menu from hardcode to text file, loads in on app start.
# TODO Dockerize

import requests
from bs4 import BeautifulSoup

def getPrimaryResults(ins:str, soup:BeautifulSoup) -> list:
    """Parse primary search command and return resulting data from search."""
    ins = ins.split(' ', 1)
    ins[1] = ins[1].replace('"', '').strip().split('=')
    return soup.find_all(ins[0], class_=ins[1][1])
    
def getDataResults(ins:str, pres:list) -> list:
    """Parse data search parameters and return resuling data."""
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
    """Format data into text columns"""
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
    text=""
    text+= f'{"Web Scraper Tool":_^40}\n'
    text+= '\t1.) Start New Search\n'
    text+= '\t2.) View Help\n'
    text+= '\t0.) Exit App\n'
    print(text)

def newSearch():
    #test_url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"

    target_url = input("Enter target url: ")
    try:
        page = requests.get(target_url)
    except Exception as e:
        print("Error occured when fetching page: ", e)
        exit()
    soup = BeautifulSoup(page.content, "html.parser")
    
    primary_input = input("Enter primary container target: ")
    primary_results = getPrimaryResults(primary_input, soup)    
    
    
    data_input = input("Enter target data: ")
    data_results = getDataResults(data_input, primary_results)

    print(formatData(data_results))

def app():
    """Main App Function for Web Scraper Tool."""
    
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