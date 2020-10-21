import requests 
from lxml import html
from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import xml.etree.ElementTree as ET
import os
from xml.dom import minidom

def format_string(g):
    str1 = ''
    for index,item in enumerate(g):
        x1 = item // 10
        x2 = item % 10
        str1 = str1 + str(x1) + str(x2)
        if index+1 != len(g):
            str1 = str1 + ' '
        else:
            return str1

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

url = 'https://www.zhcw.com/ssq/?__f=sy'

# url = 'https://free-ss.best/'

path = '//*[@class ="cz-qiu"]/span'

# driver = webdriver.Chrome()

# driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome(executable_path = r'E:\Code\execution\chromedriver\chromedriver.exe')

# response = requests.get(url)
# byte_data = response.content
# driver = webdriver.Chrome()
# driver.implicitly_wait(30)

driver.get(url)
time.sleep(5)  
res = driver.execute_script("return document.documentElement.outerHTML")

# try:
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'cz-qiu')))
# except TimeoutException:
#     print('Page timed out after 10 secs.')



# source_code = html.fromstring(res)
driver.quit()

soup = BeautifulSoup(res, 'lxml')

# check page and program
# with open('page.html', 'wb') as html_file:
#     html_file.write(res)


term = soup.find('div',{'class':'N-dq','data-v':'v1'})
term_number = term.find('strong',{'class':'N-t'})
   
#optimize display of term
term_value = term_number.text[-3:]
if term_value[0] == '0':
    term_value = term_value[-2:]


result_date = soup.find('div',{'class':'cz-rq'})
result_date_text = result_date.text.split('：')
result_date_real = result_date_text[1]
result_date_real_value = result_date_real.replace("-","/")

ball = soup.find('div',{'class':'cz-qiu'})
red_numbers = ball.find_all('span',{'class':'red'})
red_list = []
for item in red_numbers:
    red_list.append(int(item.text))

red_string = format_string(red_list)

blue_numbers = ball.find('span',{'class':'blue'})

blue_string = blue_numbers.text

with open(r'E:\Code\file\record_lottery.xml','r') as xml_file:
    tree = ET.parse(xml_file)
root = tree.getroot()

index_string = root.find('index').text
index = int(root.find('index').text)
index_key = ".//item[@number=\'{0}\']".format(index_string)
index_ele = root.find(index_key)

latest_date = index_ele.find('date').text

date1_split = result_date_real_value.split('/')
date2_split = latest_date.split('/')

date1 = datetime.date(int(date1_split[0]),int(date1_split[1]),int(date1_split[2]))
date2 = datetime.date(int(date2_split[0]),int(date2_split[1]),int(date2_split[2]))

if date1 > date2:
    root.find('index').text = str(index+1)
    elem = ET.Element('item')
    elem.set('number',str(index+1))
    elem_date = ET.Element('date')
    elem_date.text = result_date_real_value
    elem.append(elem_date)
    elem_term = ET.Element('term')
    elem_term.text = term_value
    elem.append(elem_term)
    elem_red = ET.Element('red')
    elem_red.text = red_string
    elem.append(elem_red)
    elem_blue = ET.Element('blue')
    elem_blue.text = blue_string
    elem.append(elem_blue)
    root.append(elem)
    indent(root)
    tree.write(r'E:\Code\file\record_lottery.xml',encoding="utf-8", xml_declaration=True)


# tree = source_code.xpath(path)
# s1 = tree[0].text_content()
# print(tree[0].text_content()) 