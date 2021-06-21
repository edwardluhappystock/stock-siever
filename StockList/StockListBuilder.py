from requests.models import Response
import requests
import re
import csv
import os
from lxml import etree


FOLDER_NAME = 'data'
STOCK_LIST_FILE_NAME = 'StockList.csv'
PATH_TO_STOCK_LIST = '{0}/{1}'.format(FOLDER_NAME, STOCK_LIST_FILE_NAME)

def crawl_webpage(url: str) -> Response:
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'
    headers = { 'User-Agent': user_agent }
    res = requests.get(url, headers=headers)
    return res

def process_response(response: Response) -> list:
    response.encoding = 'big5'
    html = etree.HTML(response.text)
    total_id_name_list = html.xpath("//html/body/table[2]/tr/td[1]/text()")
    return total_id_name_list

def extract_stock_id_name(total_id_name_list: list) -> list:
    re_match = r'\b[1-9]\d{3}\b'
    
    stock_id_name = []
    for item in total_id_name_list:
        match = re.search(re_match, item)
        row = []
        if match:
            row.append(item.split("\u3000")[0])
            row.append(item.split("\u3000")[1])
            stock_id_name.append(row)
            
    return stock_id_name

def save(stock_id_name: list) -> None:
    with open(PATH_TO_STOCK_LIST, 'a') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerows(stock_id_name)

def crawl_stock_list(url: str) -> list:
    response = crawl_webpage(url)
    total_list = process_response(response)
    stock_id_name = extract_stock_id_name(total_list)
    return stock_id_name

def crawl_tse_stock_list() -> None:
    tse_stock_list_url = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
    tse_stock_id_name = crawl_stock_list(tse_stock_list_url)
    save(tse_stock_id_name)

def crawl_toc_stock_list() -> None:
    toc_stock_list_url = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=4'
    toc_stock_id_name = crawl_stock_list(toc_stock_list_url)
    save(toc_stock_id_name)

def remove_old_list():
    if os.path.isfile(PATH_TO_STOCK_LIST):
       os.remove(PATH_TO_STOCK_LIST)

def create_directory():
    if(os.path.isdir(FOLDER_NAME) == False):
        os.makedirs(FOLDER_NAME)

def init():
    create_directory()
    remove_old_list()

def main():
    init()
    crawl_tse_stock_list()
    crawl_toc_stock_list()

if __name__ == '__main__':
    main()






