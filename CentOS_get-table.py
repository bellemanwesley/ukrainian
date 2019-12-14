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
from pyvirtualdisplay import Display

def capturepackets():
	try:
		os.remove('sentrequests.pcap')
	except:
		pass
	os.system("tcpdump -i enp0s3 -nn 'host lcorp.ulif.org.ua and port 80' -w sentrequests.pcap -G 8 -W 1")

def sendform(key):
	print("Block 1")
	option = Options()
	option.add_argument("--headless")
	option.add_argument('--no-sandbox')
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
	print("Block 2")

def getformdata():
	while_exit = 0
	while while_exit == 0:
		try:
			my_form_data = pyshark.FileCapture('sentrequests.pcap',display_filter='urlencoded-form')[0].http.file_data
			while_exit = 1
		except:
			print("Failure")
			return("Failure")
	t_search_start = my_form_data.find('ContentPlaceHolder1$tsearch=') + 28
	t_search_end = my_form_data.find("&",t_search_start)
	for i in range(t_search_start,t_search_end):
		if my_form_data[i] == "'":
			my_form_data = my_form_data[0:i] + "%27" + my_form_data[i+1:len(my_form_data)]

	with open('datafile.txt','w+') as datafile:
		datafile.write(my_form_data)
	print("Success")
	return(my_form_data)

def resendform(formdata,sequence,current_key):
	my_log_file = open("debug_log.txt","a")
	
	whole_html = os.popen("curl http://lcorp.ulif.org.ua/dictua/dictua.aspx -X POST -d '"+formdata+"'").read()
	current_key_correct = whole_html.find("<span class=\"word_style\" >"+current_key)

	if current_key_correct == -1:
		print("Bad Key")
		return(['nokey'])
	else:
		my_log_file.write("Key: "+current_key+"\n")
		my_log_file.close()

	table_start = whole_html.find("<div align=\"center\">")
	table_end = whole_html.find("<p class=\"comm_end_style\">",table_start)
	html_result = whole_html[table_start:table_end]
	with open('html_files/html_file'+str(sequence)+'.html','w+') as html_file:
		if html_result == "":
			html_file.write(current_key)
		else:
			html_file.write(html_result)


	next_key_start = whole_html.find(">"+current_key+"</a></td><td width=")
	word_list_start = copy.copy(next_key_start) - 1
	key_search_end = whole_html.find("</table>", next_key_start) - 65

	next_keys = []
	next_key_stop = next_key_start
	while next_key_start > word_list_start and next_key_start < key_search_end and next_key_stop > word_list_start and next_key_stop < key_search_end:
		next_key_start = whole_html.find(")\">",next_key_start) + 3
		next_key_stop = whole_html.find("</a></td><td",next_key_start)
		if next_key_start != -1 and next_key_stop != -1:
			next_key = whole_html[next_key_start:next_key_stop]

			while next_key == current_key:
				next_key_start = whole_html.find(")\">",next_key_start) + 3
				next_key_stop = whole_html.find("</a></td><td",next_key_start)
				next_key = whole_html[next_key_start:next_key_stop]
			next_keys.append(next_key)
			currrent_key = next_key	
		else:
			next_key_stop = key_search_end
	return(next_keys)

def generate_pcap(key):
		p1 = Process(target=capturepackets)
		p2 = Process(target=sendform,args=(key,))
		p1.start()
		time.sleep(0.5)
		p2.start()
		p2.join()
		time.sleep(0.5)

if __name__ == '__main__':
	display = Display(visible=0, size=(800, 800))
	display.start()

	os.system("echo '' | cat > debug_log.txt")
	keys = ["Ваа́л"]
	sequence = 0
	while keys[0][0] == 'в' or keys[0][0] == 'В':
		with open('debug_log.txt','a') as my_log_file:
			my_log_file.write("Sequence: "+str(sequence)+"    ")
		result_keys = ['nokey']
		key_i = 0
		while result_keys[0] == 'nokey':
			my_form_data = "Failure"
			while my_form_data == "Failure":
				generate_pcap(keys[key_i])
				my_form_data = getformdata()
			result_keys = resendform(my_form_data,sequence,keys[key_i])
			key_i += 1
		sequence += 1
		keys = result_keys


