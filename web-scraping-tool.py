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

import requests
from bs4 import BeautifulSoup

def parseTargetElementsInput(data:str) -> list[dict]:    
    targets = data.split("|")

    for i, each in enumerate(targets):
        targets[i] = each.strip().split(' ', 1)

    for i, each in enumerate(targets):
        each[1] = each[1].replace('"', "").split('=', 1)             

    els = []
    for target in targets:
        new_target = {}
        new_target['el'] = target[0] 
        new_target['type'] = target[1][0]
        new_target['filter'] = target[1][1]
        els.append(new_target)
            
    for each in els:
        print(each)        
    return els

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
        text+=f"{k:<width}"
    text += "\n"
    for each in data:
        for k, v in each.items():
            text += f"{v:<width}"
        text += "\n"

    return text

def app():
    """Main App Function for Web Scraper Tool."""
    test_url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
    
    try:
        page = requests.get(test_url)
    except Exception as e:
        print("Error occured when fetching page: ", e)
        exit()
    soup = BeautifulSoup(page.content, "html.parser")
    
    primary_input = input("Enter primary container target: ")
    primary_results = getPrimaryResults(primary_input, soup)    
    
    data_input = input("Enter target data: ")
    data_results = getDataResults(data_input, primary_results)

    print(formatData(data_results))
    
if __name__ == "__main__":
    app()