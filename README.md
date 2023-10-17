### Objective
Create a Terminal User Interface app that allows users to input target urls and parse for data. Web scrapping tool.

---
### Why?
This is project #4 for my AI overlords in my adventure to learn Python.

---
### How to use?
Run the app in terminal and you will be presented with a menu.
Choosing a new search will lead you through a step by step processes to fetch a site's data and parse for information
based on user specified commands.

There is a command syntax that is fairly easy to follow.

Step 1. Enter the url of the target website.
ex.
```>> https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops```

* If you want to deal with pagination the format is similar with a range of pages.
* Note that the range <1-20> is to specify which pages to get, inclusive.
ex.
```>> https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page=<1-20>```

Step 2. Enter the desired targets that contain data you want.
In the about example I aimed for name, price, description, which were all contained within the 'div' element with class 'caption'.
ex.
```>> div class="caption"```

Step 3. Enter parsing commands.
This example has 3 pieces of data to grab from the above element. Name, Price, Description. All these commands are entered in a single line use '|' to seperate.
ex.
```>> price:h4 class="float-end price card-title pull-right" | name:a class="title" attr="title" | description:p class="description card-text"```

Step 4. Save your data to a valid filetype.
The saved file is relative to the directory that the script is run.
Valid filetypes include .txt, .json, and .csv


### What was learned?
A whole lot of data validation, a whole lot of input parsing, and a little regex.

---
### TODOs List
- [X] README.md
- [ ] Dockerize
- [ ] Handle AJAZ Pagination
- [ ] Handle Load For More Button
- [ ] Handle infinite scrolling
- [ ] Add Rate Limiting Specifications
