import requests
from requests_html import HTML
import time
import pandas as pd
from selenium import webdriver
from requests_html import AsyncHTMLSession
import os

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# driver = webdriver.Chrome("./chromedriver", options=options)

chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH", chrome_options=chrome_options)


def getPageList(query, location, salary, days_ago):
    page_list = []
    for i in range(0, 100, 10):
        endpoint_orig = f"https://ca.indeed.com/jobs?q={query}&l={location}&start={i}"
        endpoint = f"https://ca.indeed.com/jobs?q={query}&l={location}&salary=%24{salary}%2C000%2B&jt=permanent&fromage={days_ago}&start={i}"
        page_list.append(endpoint)
    return page_list

def breakIntoContainers(query, location, salary, days_ago):
    page_list = getPageList(query, location, salary, days_ago)
    container_list = []
    for page in page_list:
        driver.get(page)
        body_el = driver.find_element_by_css_selector('body')
        html_str = body_el.get_attribute("innerHTML")
        html_obj = HTML(html=html_str)
        container = html_obj.xpath(".//div[@class='jobsearch-SerpJobCard unifiedRow row result clickcard']")
        for x in container:
            container_list.append(x)
    return container_list
    
    
def scrapeData(container_list):
    all_data = []
    for x in container_list:
        title = x.xpath("//h2[@class='title']")[0].text
        company = x.xpath("//span[@class='company']")[0].text
        salary = get_salary(x)
        location = get_loc(x)
        requirements = get_reqs(x)
        summary = get_summary(x)
        remote = get_remote(x)
        date = x.xpath("//span[@class='date']", first=True).text 
        link = get_link(x, container_list)
        data = {
            'date': date,
            'title': title,
            'company': company,
            'location': location,
            'salary': salary,
            'requirements': requirements,
            'summary': summary,
            'remote': remote,
            'link': link
        }
        all_data.append(data)
    return all_data

def scrapeDataTable(container_list):
    all_data = []
    for x in container_list:
        title = x.xpath("//h2[@class='title']")[0].text
        company = x.xpath("//span[@class='company']")[0].text
        salary = get_salary(x)
        location = get_loc(x)
        requirements = get_reqs(x)
        summary = get_summary(x)
        remote = get_remote(x)
        date = x.xpath("//span[@class='date']", first=True).text 
        link = get_link(x, container_list)
        data = [
            date.rsplit("d"),
            title,
            company,
            location,
            salary,
            requirements,
            summary,
            remote,
            link
        ]
        all_data.append(data)
    return all_data

    
    
def get_reqs(x):
    req = x.xpath("//div[@class='jobCardReqList']")
    if req == None:
        return "xx"
    else:
        for r in req:
            return r.text.split("\n")
                        
def get_salary(x):
    salary = x.xpath("//span[@class='salaryText']", first=True)
    if salary == None:
        return "xx"
    else:
        return salary.text
    
def get_remote(x):
    r = x.xpath(".//span[@class='remote']", first=True)
    if r == None:
        return "xx"
    else:
        return r.text
    
def get_summary(x):
    sums = x.xpath("//div[@class='summary']")[0].text
    return sums

def get_link(x, container_list):
    links_list = [x.xpath("//h2/a[@href]") for x in container_list]
    base_url = "https://ca.indeed.com"
    for slug in links_list[0][0].links:
        endpoint = f"{base_url}{slug}"
        return endpoint

def get_loc(x):
    loc = x.xpath(".//div[@class='location accessible-contrast-color-location']", first=True)
    if loc == None:
        return "xx"
    else:
        return loc.text