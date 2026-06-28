from Audit import *
import threading
from queue import Queue
from CrawlerBot.main import create_workers
from CrawlerBot.main import crawl
from CrawlerBot.domain import *
from CrawlerBot.general import *
from CrawlerBot.linkfinder import *
from CrawlerBot import spider
from general2 import *
from Scrap_Webpage import scrape
from multiprocessing import Pool
import time
import os

PROJECT_NAME = input("Project name?: ")
HOMEPAGE = input("Homepage?: ")
DOMAIN_NAME = get_domain_name(HOMEPAGE)
spider.Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

def normalize_result(result):
    if not result:
        return []

    if isinstance(result, dict):
        return list(result.items())

    if isinstance(result, list):
        # flatten nested lists safely
        flat = []
        for item in result:
            if isinstance(item, list):
                flat.extend(item)
            else:
                flat.append(item)
        return flat

    return [result]

def load_and_write_workbook(workbook_name, name_of_audit_sheet, result):
    Newbook = load_workbook(workbook_name + ".xlsx")
    Newbook.create_sheet(name_of_audit_sheet)
    worksheet = Newbook[name_of_audit_sheet]

    result_in = normalize_result(result)

    for i in range(1, len(result_in) + 1):
        worksheet.cell(row=i, column=1, value=result_in[i - 1])

    Newbook.save(filename=PROJECT_NAME + '.xlsx')
 
create_workers()
crawl(PROJECT_NAME + '/queue.txt')

# time.sleep(6)
print("Auditing")

scrapped_data = get_scrapped_data(os.path.join(PROJECT_NAME, "crawled.txt"))
duplicate_titles = scrapped_data.duplicate_titles()
duplicate_descriptions = scrapped_data.duplicate_meta_descriptions()
missing_descriptions = scrapped_data.get_missing_descriptions()
missing_titles = scrapped_data.get_missing_titles()
missing_h1 = scrapped_data.get_missing_h1()
duplicate_h1 = scrapped_data.get_duplicate_h1()
missing_canonicals = scrapped_data.get_missing_canonicals()
wrong_canonicals = scrapped_data.improper_canonicals()
missing_viewports = scrapped_data.missing_viewports()
low_titles = scrapped_data.get_titles_with_less_content()
low_meta = scrapped_data.get_meta_des_with_less_content()

print("Duplicate Titles:", duplicate_titles)
print("Duplicate Meta:", duplicate_descriptions)
print("Missing Descriptions:", missing_descriptions)
print("Missing Titles:", missing_titles)
print("Missing H1:", missing_h1)
print("Duplicate H1:", duplicate_h1)
print("Missing Canonicals:", missing_canonicals)
print("Improper Canonicals:", wrong_canonicals)
print("Missing Viewports:", missing_viewports)
print("Thin Titles:", low_titles)
print("Thin Meta:", low_meta)
print("Preparing Results")

create_workbook(PROJECT_NAME)

load_and_write_workbook(PROJECT_NAME, 'DuplicateTitles', duplicate_titles)
load_and_write_workbook(PROJECT_NAME, 'DuplicateMetaDescriptions', duplicate_descriptions)
load_and_write_workbook(PROJECT_NAME, 'missingDescriptions', missing_descriptions)
load_and_write_workbook(PROJECT_NAME, 'Thin Meta', low_meta)
load_and_write_workbook(PROJECT_NAME, 'thin titles', low_titles)
load_and_write_workbook(PROJECT_NAME, 'Missing Viewports', missing_viewports)
