from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import pyshark
import time
import os
from multiprocessing import Process
import copy

def capturepackets():
	try:
		os.remove('ignore_files/sentrequests.pcap')
	except:
		pass
	os.system("tcpdump -i en0 -nn 'host lcorp.ulif.org.ua and port 80' -w ignore_files/sentrequests.pcap -G 7 -W 1")

def clickfirst(key):
	option = Options()
	option.add_argument("--headless")
	#option.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

	browser = webdriver.Chrome(executable_path='../tools/chromedriver', options=option)
	browser.get("http://lcorp.ulif.org.ua/dictua/")

	# get the text submission element
	text_element = browser.find_element_by_name("ctl00$ContentPlaceHolder1$tsearch")
	text_element.clear()
	text_element.send_keys(key)

	# get the submit button element
	submit_element = browser.find_element_by_name("ctl00$ContentPlaceHolder1$search")
	submit_element.click()

	# get the nextpage button element, click it
	submit_element = browser.find_element_by_name("ctl00$ContentPlaceHolder1$nextpage")
	submit_element.click()

	# get the nextpage button element, click it
	submit_element = browser.find_element_by_name("ctl00$ContentPlaceHolder1$nextpage")
	submit_element.click()

	# get the nextpage button element, click it
	submit_element = browser.find_element_by_name("ctl00$ContentPlaceHolder1$nextpage")
	submit_element.click()

def getformdata():
	while_exit = 0
	while while_exit == 0:
		try:
			my_form_data = pyshark.FileCapture('ignore_files/sentrequests.pcap',display_filter='urlencoded-form')[3].http.file_data
			while_exit = 1
		except:
			print("Failure")
			return("Failure")
	t_search_start = my_form_data.find('ContentPlaceHolder1$tsearch=') + 28
	t_search_end = my_form_data.find("&",t_search_start)
	for i in range(t_search_start,t_search_end):
		if my_form_data[i] == "'":
			my_form_data = my_form_data[0:i] + "%27" + my_form_data[i+1:len(my_form_data)]

	#with open('ignore_files/datafile.txt','w+') as datafile:
		#datafile.write(my_form_data)
	print("Success")
	return(my_form_data)

def resendform(formdata):
	whole_html = os.popen("curl http://lcorp.ulif.org.ua/dictua/dictua.aspx -X POST -d '"+formdata+"'").read()
	return whole_html



if __name__ == '__main__':
	key = 'а'
	my_form_data = "Failure"
	while  my_form_data == "Failure":
		p1 = Process(target=capturepackets)
		p2 = Process(target=clickfirst,args=(key,))
		p1.start()
		time.sleep(0.5)
		p2.start()
		p2.join()
		time.sleep(0.5)
		my_form_data = getformdata()
	print(resendform(my_form_data))



