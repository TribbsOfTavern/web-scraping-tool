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
# TODO README.md
# TODO Dockerize
# TODO Handle AJAZ Pagination
# TODO Handle Load For More Button
# TODO Handle infinite scrolling
# TODO Add Rate Limiting Specifications


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
    for i, cmd in enumerate(ins):
        ins[i] = cmd.strip()
    
    for cmd in ins:
        attempt = ()
        if "attr=\"" in cmd:
            attempt = re.findall("^(\w+):(\w+) class=\"(.*?)\" attr=\"(.*?)\"", cmd)
        else:
            
            attempt = re.findall("^(\w+):(\w+) class=\"(.*?)\"", cmd)
        if not attempt:
            return False
        else:
            if len(attempt[0]) == 3:
                if attempt[0][2].strip() == "": return False
            elif len(attempt[0]) == 4:
                if attempt[0][2].strip() == "": return False
                if attempt[0][3].strip() == "": return False
    return True

def getPageRequest(ins:str) -> bytes | list:
    pages = re.findall("<(\d+)-(\d+)>", ins)
    if pages:
        responses = []
        start_page = int(pages[0][0])
        end_page = int(pages[0][1])
        page_count = 0
        while start_page + page_count <= end_page:
            url = ins.split("<", 1)[0] + str(start_page + page_count) + ins.split('>', 1)[1]
            try:
                print(f"Targetting {url}...")
                response = requests.get(url)
                if response.status_code == 200:
                    responses.append(response.content)
                else:
                    invalidInput(f"Failed Response Code: {response.status_code}\n{page_count} pages gathered.")
                    break
            except Exception as e:
                invalidInput(f"Error occurred during page request: {e}")
                break
            page_count += 1
        return responses if responses else False
    
    else:
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

def getPrimarySoup(ins:str, content) -> list:
    results = []
    elements = ins.split(' ', 1)[0].strip()
    classes = ins.split('=')[1].replace('"', '').strip()
    if type(content) == list:
        for page in content:
            parsed = BeautifulSoup(page, "html.parser")
            for found in parsed.find_all(elements, class_=classes):
                results.append(found)
            print(f"{len(results)} found...")
            
    else:
        print('single url')
        parsed = BeautifulSoup(content, "html.parser")
        for found in parsed.find_all(elements, class_=classes):
            results.append(found)
        print(f"{len(results)} found...")

    return results

def getDataSearchResults(ins:str, primary_results:list):
    ins = ins.split('|')
    for i, e in enumerate(ins):
        ins[i] = e.strip()
    
    results = []
    print("Parsing Data...", end="")
    for each in primary_results:
        new_res = {}
        for cmd in ins:
            info = None
            if "attr=" in cmd:
                info = re.findall("^(\w+):(\w+) class=\"(.*?)\" attr=\"(.*?)\"$", cmd)
            else:
                info = re.findall("^(\w+):(\w+) class=\"(.*?)\"$", cmd)
            
            if len(info[0]) == 3:
                new_res[info[0][0]] = each.find(info[0][1], class_=info[0][2]).text
            if len(info[0]) == 4:
                new_res[info[0][0]] = each.find(info[0][1], class_=info[0][2])[info[0][3]]
    
        results.append(new_res)
        
    print(f"{len(results)}")
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

def saveFileAs(filename:str, data:list) -> bool:
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
                return True
            if file_ext == 'json':
                with open(filename, 'w') as wf:
                    json.dump(data, wf, indent=4)
                return True
            if file_ext == 'csv':
                with open(filename, "w") as wf:
                    writer = csv.writer(wf, delimiter='|')
                    for line in data:
                        row = []
                        for item in line:
                            row.append(line[item])
                        writer.writerow(row)
                return True
        except Exception as e:
            print(e)
            invalidInput(f"Error Saving File {filename}: {e}")
            return False
                
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

                while scraping:
                    clearTerminal()
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
                    inp = input("Enter primary search command: ")
                    if inp != "-1" and validPrimaryCmd(inp):
                        curr_primary_cmd = inp
                        curr_soup = getPrimarySoup(inp, curr_page)
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
                    if inp != "-1" and not validDataSearchCmd(inp):
                        invalidInput('Invalid data parse command syntax. <datatitle>:<element> class="<classes>".\nSeperate commands with |.')                        
                        clearTerminal()
                    if inp == "-1":
                        break
                    
                    # Ask user for preferred output method
                    print("Enter a filename with extention to output file.")
                    print("Valid extentsion: .txt .json .csv")
                    inp = input(">> ")
                    saved = saveFileAs(inp, data)
                    if saved:
                        print(f"file \"{inp}\" saved successfully.")
                    
                    print("Would you like to do another search? (y/n)")
                    inp = input(">> ")
                    if inp != "y" or inp != "yes":
                        break
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
