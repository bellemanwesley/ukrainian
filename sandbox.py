import os


def resendform(formdata,sequence,current_key):
	my_log_file = open("debug_log.txt","a")
	whole_html = os.popen("curl http://lcorp.ulif.org.ua/dictua/dictua.aspx -X POST -d '"+formdata+"'").read()
	table_start = whole_html.find("<div align=\"center\">")
	table_end = whole_html.find("<p class=\"comm_end_style\">",table_start)
	html_result = whole_html[table_start:table_end]
	html_log = open("received_html"+str(sequence)+".txt","w+")
	html_log.write(whole_html)
	with open('html_files/html_file'+str(sequence)+'.html','w+') as html_file:
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

my_file = open('received_html74.txt','r').read()
print(resendform(my_file,74,'Абе'))