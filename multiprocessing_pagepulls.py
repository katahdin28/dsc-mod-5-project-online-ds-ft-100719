from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import json
import datetime
from itertools import repeat
from time import sleep, time
from multiprocessing import Pool, cpu_count
from multiprocessing import Queue,Process
import queue

option = webdriver.ChromeOptions()
option.add_argument('--headless')

browser = webdriver.Chrome(options = option)
browser.get('https://www.winespectator.com/auth/login')

username = browser.find_element_by_name("userid")
username.clear()
username.send_keys('johnmkline@gmail.com')

password = browser.find_element_by_name("passwd")
password.clear()
password.send_keys('ohnomoose')

browser.find_element_by_id("target").click()

def get_text(sixdigstring):
    browser.get(f'https://www.winespectator.com/wine/detail/source/search/note_id/{sixdigstring}')
    full_site = browser.find_element_by_class_name("main-layout")
    text_string = full_site.text
    text_string = text_string[:text_string.find('Add this wine to this Personal Wine List')]
    return text_string

def iterate_pages(index_list,index_number):
    index0_num = int(index_list[0])
    list_len = len(index_list)
    with open(f'raw_reviews_{index_number}.txt','w') as file:
        file.write("{")
        for string in index_list:
            file.write(string+' : '+get_text(string)+", ")
        file.write("'end': None}")

def load_object(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return(data)

remaining_index = load_object('remaining_index.json')

dict_of_lists = {}
pages_per_process = 2000
for i in range(8):
    temp_list = remaining_index[i*pages_per_process:(i+1)*pages_per_process-1]
    dict_of_lists[i] = temp_list

def run_process(index_list,index_number):
    iterate_pages(index_list, index_number)

if __name__ == '__main__':
    p1 = Process(target=run_process, args = (dict_of_lists[0],0,))
    p1.start()
    p2 = Process(target=run_process, args = (dict_of_lists[1],1,))
    p2.start()
    p3 = Process(target=run_process, args = (dict_of_lists[2],2,))
    p3.start()
    p4 = Process(target=run_process, args = (dict_of_lists[3],3,))
    p4.start()
    p5 = Process(target=run_process, args = (dict_of_lists[4],4,))
    p5.start()
    p6 = Process(target=run_process, args = (dict_of_lists[5],5,))
    p6.start()
    p7 = Process(target=run_process, args = (dict_of_lists[6],6,))
    p7.start()
    p8 = Process(target=run_process, args = (dict_of_lists[7],7,))
    p8.start()
    p8.join()
    p7.join()
    p6.join()
    p5.join()
    p4.join()
    p3.join()
    p2.join()
    p1.join()

print("Finished!")