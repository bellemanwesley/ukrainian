from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import pyshark
import time
import os

def sendform():
	option = Options()
	option.add_argument("--headless")
	option.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

	browser = webdriver.Chrome(executable_path='/Users/wesley/Documents/Personal Development/IT/Ukrainian/chromedriver', options=option)
	browser.get("http://lcorp.ulif.org.ua/dictua/")

	# get the text submission element
	text_element = browser.find_element_by_name("ctl00$ContentPlaceHolder1$tsearch")
	text_element.clear()
	text_element.send_keys("сука")

	# get the submit button element
	submit_element = browser.find_element_by_name("ctl00$ContentPlaceHolder1$search")
	submit_element.click()

	time.sleep(6)

def wireshark():
	wireshark_processes = os.popen("ps -ax | grep Wireshark").readlines()
	pids = []
	for x in wireshark_processes:
		pids.append(x.split(' ')[0])

	#for x in pids:
		#os.system('kill -KILL '+x)

	cap = pyshark.FileCapture('sentrequests.pcap',display_filter='urlencoded-form')
	with open('formdata.txt','w+') as formdata:
		formdata.write(cap[0].http.file_data)
		#print(cap[0].http.file_data)