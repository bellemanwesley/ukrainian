#!/usr/local/bin/python3.8

import os
import boto3
import json
import copy
from shutil import copyfile
from datetime import date
import re
import time

letter_order = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюяа́я́е́є́и́і́ї́о́у́ю́'
cap_letter_order = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯА́Я́Е́Є́И́І́Ї́О́У́Ю́'

def get_page():
	main_page = os.popen("curl https://ua.korrespondent.net/").read()
	search_index = main_page.find("<div class=\"article_main\">")
	link_start = main_page.find("href=\"",search_index) + 6
	link_end = main_page.find("\">",link_start)
	link = main_page[link_start:link_end]
	article_page = os.popen("curl "+link).read()
	del(main_page)
	article_start = article_page.find("<div class=\"post-item__text\">")
	article_page = article_page[article_start:len(article_page)]
	article_content = remove_tags(article_page)
	article_end = article_content.find("Новини від Корреспондент.net")
	article_content = article_content[0:article_end]
	return article_content

def remove_tags(html):
	con = True
	search_start = 0
	while con:
		tag_begin = html.find("<script",search_start)
		tag_end = html.find("</script>",tag_begin) +9
		if tag_begin == -1 or tag_end == -1:
			con = False
		else:
			html_list = list(html)
			del(html_list[tag_begin:tag_end])
			html = ''.join(html_list)
			search_start = copy.copy(tag_begin)
	con = True
	search_start = 0
	while con:
		tag_begin = html.find("<",search_start)
		tag_end = html.find(">",tag_begin) + 1
		if tag_begin == -1 or tag_end == -1:
			con = False
		else:
			html_list = list(html)
			del(html_list[tag_begin:tag_end])
			html = ''.join(html_list)
			search_start = copy.copy(tag_begin)
	return html

def pull_dicts():
	try:
		os.system("mkdir ignore_files")
	except:
		pass
	try:
		os.system("mkdir ignore_files/dicts")
	except:
		pass
	print
	for letter in cap_letter_order+letter_order:
		print(letter + " " + str(letter.encode('utf-8')))
		new_json = os.popen("curl https://ukrainian-words.s3.us-east-2.amazonaws.com/%"+str(letter.encode('utf-8'))[4:6]+"%"+str(letter.encode('utf-8'))[8:10]+".json").read()
		if new_json.find("Access Denied") == -1:
			with open("ignore_files/dicts/"+letter+".json","w+") as new_file:
				new_file.write(new_json)

def replace_words(page):
	page_list = page.split(" ")
	for i in range(len(page_list)):
		try:
			word_json = open("ignore_files/dicts/"+page_list[i][0]+".json","r")
			word_dict = json.loads(word_json.read())
			word_json.close()
			page_list[i] = word_dict[page_list[i]]['accent']
		except:
			pass
	return " ".join(page_list)

def write_html(text_content):
	text_content = re.sub(r'\s*\n\s*','</p><p>',text_content)
	words = len(re.findall(r'\S+'))
	goal1 = str(words // 120) + ":" + str(int(60*(words/120.0-words//120)))
	goal2 = str(words // 200) + ":" + str(int(60*(words/200.0-words//200)))
	text_list = re.split(r'\n+',text_content)	
	html_text = "<html><head><link rel=\"stylesheet\" href=\"articles.css\"></head><body>"
	html_text = html_text + "<iframe src=\"http://ipadstopwatch.com/embed.html\" frameborder=\"0\" scrolling=\"no\" width=\"391\" height=\"140\"></iframe>"
	html_text = html_text + "<div id=\"div0\"><p>" + str(words)  +" Words</p><p>goal 1: "+str(goal1) +"<button>Complete</button></p><p>goal 2: " + str(goal2) +  "<button>Complete</button></p></div>"
	html_text = html_text + "<div id=\"div1\"><p>"
	html_text = html_text + "</p></div></body></html>"
	html_file = open('new_page.html','w+')
	html_file.write(html_text)
	html_file.close()

def main():
	pull_dicts()
	page = get_page()
	page = replace_words(page)
	write_html(page)
	os.system("sudo cp new_page.html /var/www/html/articles/"+str(date.today())+".html")
	os.system("sudo cp articles.css /var/www/html/articles/articles.css")

if __name__ == '__main__':
	#with open('ignore_files/test_page.txt','r') as page_file:
	#write_html(page_file.read())
	#with DaemonContext():
	main()


