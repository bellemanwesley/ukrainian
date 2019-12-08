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

def capturepackets():
	try:
		os.remove('sentrequests.pcap')
	except:
		pass
	os.system("wireshark -i en0 -f 'host lcorp.ulif.org.ua and port 80' -k -w sentrequests.pcap -a duration:7")

def sendform(key,count):
	option = Options()
	option.add_argument("--headless")
	option.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

	browser = webdriver.Chrome(executable_path='/Users/wesley/Documents/Personal Development/IT/Ukrainian/chromedriver', options=option)
	browser.get("http://lcorp.ulif.org.ua/dictua/")

	# get the text submission element
	text_element = browser.find_element_by_name("ctl00$ContentPlaceHolder1$tsearch")
	text_element.clear()
	text_element.send_keys(key)

	# get the submit button element
	submit_element = browser.find_element_by_name("ctl00$ContentPlaceHolder1$search")
	submit_element.click()

	wireshark_processes = os.popen("ps -ax | grep Wireshark").readlines()
	pids = []

	for x in wireshark_processes:
		pids.append(x.split(' ')[0])
		if count > 3:
			pass
			for i in range(len(pids)-4):
				os.system("kill -KILL "+pids[i])

def getformdata():
	cap = pyshark.FileCapture('sentrequests.pcap',display_filter='urlencoded-form')

	try:
		with open('datafile.txt','w+') as datafile:
			datafile.write(cap[0].http.file_data)
		print("Success")
		#print(cap[0].http.file_data)
		return(cap[0].http.file_data)
	except:
		print("Failure")
		return("Failure")

def resendform(formdata,sequence,current_key):
	my_log_file = open("debug_log.txt","a")
	whole_html = os.popen("curl http://lcorp.ulif.org.ua/dictua/dictua.aspx -X POST -d '"+formdata+"'").read()
	table_start = whole_html.find("<div align=\"center\">")
	table_end = whole_html.find("<p class=\"comm_end_style\">",table_start)
	html_result = whole_html[table_start:table_end]
	with open('html_files/html_file'+str(sequence)+'.html','w+') as html_file:
		if html_result == "":
			html_file.write(current_key)
		else:
			html_file.write(html_result)

	word_list_start = whole_html.find(">Реєстр</th><th scope=")
	current_key_start = whole_html.find(">"+current_key+"</a></td><td width=")

	next_key_start = whole_html.find(")\">",current_key_start) + 3
	next_key_stop = whole_html.find("</a></td><td width=",next_key_start)
	next_key = whole_html[next_key_start:next_key_stop]
	print("Start:"+str(next_key_start)+"   Stop:"+str(next_key_stop)+"   Key:"+next_key)
	while next_key == current_key:
		next_key_start = whole_html.find(")\">",next_key_start) + 3
		next_key_stop = whole_html.find("</a></td><td width=",next_key_start)
		next_key = whole_html[next_key_start:next_key_stop]		

	my_log_file.write("Key info: "+current_key+"  "+str(next_key_start)+"  "+str(next_key_stop)+"  "+next_key+"\n")
	return(next_key)

if __name__ == '__main__':
	os.system("echo '' | cat > debug_log.txt")
	key = 'аб\'юра́ція'
	sequence = 323
	count = 0
	while sequence < 260000:
		p1 = Process(target=capturepackets)
		#print(key)
		p2 = Process(target=sendform,args=(key,count))
		p1.start()
		time.sleep(0.5)
		p2.start()
		p2.join()
		time.sleep(0.5)
		my_form_data = getformdata()
		if my_form_data != "Failure":
			key = resendform(my_form_data,sequence,key)
			#print(key)
			sequence += 1
			with open('debug_log.txt','a') as my_log_file:
				my_log_file.write("Sequence:  "+str(sequence)+"  ")
		count += 1
	#print(resendform(getformdata(),sequence))


