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
#   OPTIONAL: Add handling for different file types
#       Currently: JSON TXT CSV
#   
#   CHATTER SUGGEST: Dockerize
#   CHATTER SUGGEST: TUI - Terminal User Interface
#   TEST SITE: https://webscraper.io/test-sites
#   TARGET URL: https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops
#      PRIMARY ELEMENT: div class="card-body"
#      DATA CMDS: name:a class="title" | price:h4 class="float-end price card-title pull-right" | desc:p class="description card-text"
#-- TODO url validation
#-- TODO request error handling
#-- TODO primary search user input validation
#-- TODO data parse target data input validation
# TODO data parse get text AND attributes
# TODO handle pagenition
# TODO error handling for missing data
# TODO README.md
#-- TODO user specify output file and output type
#-- TODO move help menu from hardcode to text file, loads in on app start.
# TODO Dockerize

import requests
import re
import os
import json
import csv
import platform
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def clearTerminal():
    if platform.system() == "Windows": os.system('cls')    
    if platform.system() == "Linux": os.system('clear')
    if platform.system() == "Darwin": os.system('clear')

def validURL(url:str) -> bool:
    url = url.lower()
    return True if (urlparse(url).scheme == "http" or urlparse(url).scheme == "https") and urlparse(url).netloc else False

def validPrimaryCmd(ins:str) -> bool:
    attempt = re.findall("^(\\w+) class=\"(.*?)\"$", ins)
    if not attempt: return False
    if attempt and attempt[0][1].strip() == "": return False                      
    return True

def validDataSearchCmd(ins:str) -> bool:
    ins = ins.split('|')
    for i, e in enumerate(ins):
        ins[i] = e.strip()
    
    for each in ins:
        attempt = re.findall("^(\w+):(\w+) class=\"(.*?)\"$", each)
        if not attempt: return False
        if attempt and attempt[0][2].strip() == "": return False
    return True

def getPageRequest(ins:str) -> requests.Response.content:
    try:
        response = requests.get(ins)
        if response.status_code == 200:
            return response.content
        else:
            invalidInput(f"Failed Response Code: {response.status_code}")
            return False
    except Exception as e:
        invalidInput(f"Error occurred during page request: {e}")
        return False

def getPrimarySoup(ins:str, soup:BeautifulSoup) -> list:
    elements = ins.split(' ', 1)[0].strip()
    classes = ins.split('=')[1].replace('"', '').strip()
    return soup.find_all(elements, class_=classes)

def getDataSearchResults(ins:str, primary_results:list):
    ins = ins.split('|')
    for i, e in enumerate(ins):
        ins[i] = e.strip()
    
    results = []
    for each in primary_results:
        new_res = {}
        for cmd  in ins:
            info = re.findall("^(\w+):(\w+) class=\"(.*?)\"$", cmd)
            new_res[info[0][0]] = each.find(info[0][1], class_=info[0][2]).text
        results.append(new_res)
    return results

def displayHelp():
    with open('scraperhelp.txt', 'r') as f:
        text = f.read()
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

def saveFileAs(filename:str, data:list):
    extentions = ['txt', 'json', 'csv']
    file_ext = filename.split('.')[-1]
    if file_ext in extentions:
        try:
            if file_ext == 'txt':
                with open(filename, 'w') as wf:
                    text = ""
                    for line in data:
                        for i, item in enumerate(line):
                            text += f"{line[item]:<30}"
                        text += '\n'
                    wf.write(text)
                    
            if file_ext == 'json':
                with open(filename, 'w') as wf:
                    json.dump(data, wf, indent=4)
            if file_ext == 'csv':
                with open(filename, "w") as wf:
                    writer = csv.writer(wf, delimiter='|')
                    for line in data:
                        row = []
                        for item in line:
                            row.append(line[item])
                        writer.writerow(row)
        except Exception as e:
            print(e)
            invalidInput(f"Error Saving File {filename}: {e}")
                
def app():
    exit_app = False
    curr_page = None
    curr_soup = None
    curr_target_url = None
    curr_primary_cmd = None
    curr_data_commands = None
    
    while not exit_app:
        clearTerminal()
        displayMenu()
        opt = input(">> ")
        match opt:
            case "0":
                exit_app = True
            case "1":
                scraping = True
                first_search = True
                while scraping:
                    clearTerminal()
                    if first_search:
                        print("-1 at any input will return to main menu.")
                        inp = input("Enter target URL: ")
                        if inp != '-1' and validURL(inp): 
                            curr_target_url = inp
                            first_search = False
                            curr_page = getPageRequest(curr_target_url)
                            if not curr_page:
                                break
                        if inp != "-1" and not validURL(inp):
                            invalidInput("Invalid URL target, recheck and dont forget http and https.")
                            clearTerminal()
                        if inp == "-1":
                            clearTerminal()
                            break
                    
                    # Ask user for primary target search
                    if not first_search:
                        print(f"Current Target: {curr_target_url}")
                    inp = input("Enter primary search command: ")
                    if inp != "-1" and validPrimaryCmd(inp):
                        curr_primary_cmd = inp
                        curr_soup = getPrimarySoup(inp, BeautifulSoup(curr_page, "html.parser"))
                    # If user input is invalid - shout at them
                    if inp != "-1" and not validPrimaryCmd(inp):
                        invalidInput('Invalid primary search syntax. <element> class="<classes>".')
                        clearTerminal()
                    if inp == "-1":
                        clearTerminal()
                        break
                    
                    # Ask user for data parse commands
                    inp = input("Enter data parse commands: ")
                    if inp != "-1" and validDataSearchCmd(inp):
                        curr_data_commands = inp
                        data = getDataSearchResults(inp, curr_soup)
                        # If user input it invalid - shout at them
                    if inp != "-1" and validDataSearchCmd(inp):
                        invalidInput('Invalid data parse command syntax. <datatitle>:<element> class="<classes>".\nSeperate commands with |.')                        
                        clearTerminal()
                    if inp == "-1":
                        break
                    
                    # Ask user for preferred output method
                    print("Enter a filename with extention to output file.")
                    print("Valid extentsion: .txt .json .csv")
                    inp == input(">> ")
                    saveFileAs(inp)
            case "2":
                displayHelp()
                invalidInput("")
                clearTerminal()
            case _:
                invalidInput("Please choose a valid option.")
                clearTerminal()
                
    print("Exiting Webscraper Tool...")

if __name__ == "__main__":
    app()