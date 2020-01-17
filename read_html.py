import os
import json
import copy
from shutil import copyfile

master_file = open('ignore_files/word_files/master.json','r')
master_dict = json.loads(master_file.read())
master_file.close()
completed_files = []

def program_exit(message):
	master_file = open('ignore_files/word_files/master.json','w+')
	master_file.write(json.dumps(master_dict,ensure_ascii=False))
	master_file.close()
	for x in completed_files:
		os.system('mv ignore_files/html_files/'+x+' ignore_files/completed_html_files/'+x)
	print(message)

def generate_table(file_text):
	word_type_start = file_text.find("gram_style") + 14
	word_type_stop = file_text.find("</span>",word_type_start)
	if word_type_start == -1 or word_type_stop == -1:
		return([['other',file_text]])
	word_type = file_text[word_type_start:word_type_stop]
	root_start = file_text.find("word_style") + 13
	root_stop = file_text.find("</span>",root_start) - 1
	root = file_text[root_start:root_stop].encode('utf-8').replace(b'\xCC\x81',b'').decode('utf-8')
	table = [[word_type,root]]
	file_text = ''.join(file_text.split(" "))
	file_text = ''.join(file_text.split("\n"))
	file_text = ''.join(file_text.split("\t"))
	file_text = ''.join(file_text.split("*"))
	rowsearch = file_text.find("<tr")
	while rowsearch != -1:
		rowbegin = file_text.find(">",rowsearch) + 1
		rowend = file_text.find("</tr>",rowbegin)
		row = file_text[rowbegin:rowend]
		entrysearch = row.find("<td")
		row_list = []
		while entrysearch != -1:
			entrybegin = row.find(">",entrysearch) + 1
			entryend = row.find("<",entrybegin)
			entry = row[entrybegin:entryend]
			row_list.append(entry)
			entrysearch = row.find("<td",entryend)
		rowsearch = file_text.find("<tr",rowend)
		table.append(row_list)
	return(table)

def build_dict_noun(table):
	result_dict = {}
	root = table[0][1]
	for i in range(2,len(table)):
		for j in range(1,len(table[i])):
			key_text = table[i][j]
			if key_text.find(",") != -1:
				keys = key_text.split(",")
			else:
				keys = [key_text]
			for key in keys:
				accent = copy.copy(key)
				key = key.encode('utf-8').replace(b'\xCC\x81',b'').decode('utf-8')
				if len(key) > 4:
					if key[0:4] == "на/в" or key[0:4] == "на/у":
						key = key[4:len(key)]
						accent = accent[4:len(accent)]
					elif key[0:4] == "по" + root[0:2] or key[0:4] == "на" + root[0:2]:
						key = key[2:len(key)]
						accent = accent[2:len(accent)]
					elif key[0:5] == "уна/у":
						key = key [5:len(key)]
						accent = accent[5:len(accent)]					
				temp_dict = {key:{'accent':accent,'case':table[i][0],'plural':table[1][j],'part':table[0][0],'root':root}}
				if key != "&nbsp;" and key not in result_dict:
					result_dict.update(temp_dict)
				elif key in result_dict:
					for x in result_dict[key]:
						if result_dict[key][x] != temp_dict[key][x]:
							result_dict[key].update({x:result_dict[key][x]+','+temp_dict[key][x]})
	return result_dict

def build_dict_verb(table):
	result_dict = {}
	root = table[0][1]
	for i in range(2,len(table)):
		for j in range(1,len(table[i])):
			key_text = table[i][j]
			if key_text.find(",") != -1:
				keys = key_text.split(",")
			else:
				keys = [key_text]
			for key in keys:
				accent = copy.copy(key)
				key = key.encode('utf-8').replace(b'\xCC\x81',b'').decode('utf-8')
				temp_dict = {key:{'accent':accent,'case':table[i][0],'plural':table[1][j],'part':table[0][0],'root':root}}
				if key != "&nbsp;" and key not in result_dict:
					result_dict.update(temp_dict)
				elif key in result_dict:
					for x in result_dict[key]:
						if result_dict[key][x] != temp_dict[key][x]:
							result_dict[key].update({x:result_dict[key][x]+','+temp_dict[key][x]})

	print(table)
	print(result_dict)

def build_dict_adjective(table):
	result_dict = {}
	root = table[0][1]
	for i in range(2,len(table)):
		for j in range(1,len(table[i])):
			key_text = table[i][j]
			if key_text.find(",") != -1:
				keys = key_text.split(",")
			else:
				keys = [key_text]
			for key in keys:
				accent = copy.copy(key)
				key = key.encode('utf-8').replace(b'\xCC\x81',b'').decode('utf-8')
				if len(key) > 4:
					if key[0:4] == "на/в" or key[0:4] == "на/у":
						key = key[4:len(key)]
						accent = accent[4:len(accent)]
					elif key[0:4] == "по" + root[0:2] or key[0:4] == "на" + root[0:2]:
						key = key[2:len(key)]
						accent = accent[2:len(accent)]
					elif key[0:5] == "уна/у":
						key = key [5:len(key)]
						accent = accent[5:len(accent)]					
				temp_dict = {key:{'accent':accent,'case':table[i][0],'plural':table[1][j//4+1],'part':table[0][0],'root':root}}
				if j < 4:
					temp_dict[key].update({'gender':table[2][j-1]})
				if key != "&nbsp;" and key not in result_dict:
					result_dict.update(temp_dict)
				elif key in result_dict:
					for x in result_dict[key]:
						if x not in temp_dict[key]:
							result_dict[key].update({x:result_dict[key][x]+','})							
						elif result_dict[key][x] != temp_dict[key][x]:
							result_dict[key].update({x:result_dict[key][x]+','+temp_dict[key][x]})
	return result_dict

def build_dict_imperf_verb(table):
	result_dict = {}
	infinitive_key = copy.copy(table[1][1].encode('utf-8').replace(b'\xCC\x81',b'').decode('utf-8'))
	result_dict.update({infinitive_key:{'tense':table[1][0],'accent':table[1][1],'part':table[0][0],'root':table[0][1]}})
	for i in [4,5,7,8,9,11,12,13]:
		for j in range(1,len(table[i])):
			key_text = table[i][j]
			if key_text.find(",") != -1:
				keys = key_text.split(",")
			else:
				keys = [key_text]
			for key in keys:
				accent = copy.copy(key)
				if i < 6:
					tense_index = 3
				elif 6 < i < 10:
					tense_index = 6
				elif i > 10:
					tense_index = 10
				key = key.encode('utf-8').replace(b'\xCC\x81',b'').decode('utf-8')
				temp_dict = {key:{'accent':accent,'tense':table[tense_index][0],'subject':table[i][0],'part':table[0][0],'root':table[0][1],'plural':table[2][j]}}
				if key != "&nbsp;" and key not in result_dict:
					result_dict.update(temp_dict)
				elif key in result_dict:
					for x in result_dict[key]:
						if x not in temp_dict[key]:
							result_dict[key].update({x:result_dict[key][x]+','})							
						elif result_dict[key][x] != temp_dict[key][x]:
							result_dict[key].update({x:result_dict[key][x]+','+temp_dict[key][x]})
	for i in [15,17,23,25,27,29]:
		key_text = table[i][0]
		if key_text.find(",") != -1:
			keys = key_text.split(",")
		else:
			keys = [key_text]
		for key in keys:
			accent = copy.copy(key)
			key = key.encode('utf-8').replace(b'\xCC\x81',b'').decode('utf-8')
			temp_dict = {key:{'accent':accent,'tense':table[i-1][0],'part':table[0][0],'root':table[0][1]}}
			if key != "&nbsp;" and key not in result_dict:
				result_dict.update(temp_dict)
			elif key in result_dict:
				for x in result_dict[key]:
					if x not in temp_dict[key]:
						result_dict[key].update({x:result_dict[key][x]+','})							
					elif result_dict[key][x] != temp_dict[key][x]:
						result_dict[key].update({x:result_dict[key][x]+','+temp_dict[key][x]})
	for i in [19,20,21]:
		for j in range(1,len(table[i])):
			key_text = table[i][j]
			if key_text.find(",") != -1:
				keys = key_text.split(",")
			else:
				keys = [key_text]
			for key in keys:
				accent = copy.copy(key)
				key = key.encode('utf-8').replace(b'\xCC\x81',b'').decode('utf-8')
				temp_dict = {key:{'accent':accent,'tense':table[18][0],'part':table[0][0],'root':table[0][1],'plural':table[2][j]}}
				if j == 1:
					temp_dict[key].update({'gender':table[i][0]})			
				if key != "&nbsp;" and key not in result_dict:
					result_dict.update(temp_dict)
				elif key in result_dict:
					for x in result_dict[key]:
						if x not in temp_dict[key]:
							result_dict[key].update({x:result_dict[key][x]+','})							
						elif result_dict[key][x] != temp_dict[key][x]:
							result_dict[key].update({x:result_dict[key][x]+','+temp_dict[key][x]})
	return result_dict

def build_dict_perf_verb(table):
	result_dict = {}
	infinitive_key = copy.copy(table[1][1].encode('utf-8').replace(b'\xCC\x81',b'').decode('utf-8'))
	result_dict.update({infinitive_key:{'tense':table[1][0],'accent':table[1][1],'part':table[0][0],'root':table[0][1]}})
	for i in [4,5,7,8,9]:
		for j in range(1,len(table[i])):
			key_text = table[i][j]
			if key_text.find(",") != -1:
				keys = key_text.split(",")
			else:
				keys = [key_text]
			for key in keys:
				accent = copy.copy(key)
				if i < 6:
					tense_index = 3
				elif 6 < i:
					tense_index = 6
				key = key.encode('utf-8').replace(b'\xCC\x81',b'').decode('utf-8')
				temp_dict = {key:{'accent':accent,'tense':table[tense_index][0],'subject':table[i][0],'part':table[0][0],'root':table[0][1],'plural':table[2][j]}}
				if key != "&nbsp;" and key not in result_dict:
					result_dict.update(temp_dict)
				elif key in result_dict:
					for x in result_dict[key]:
						if x not in temp_dict[key]:
							result_dict[key].update({x:result_dict[key][x]+','})							
						elif result_dict[key][x] != temp_dict[key][x]:
							result_dict[key].update({x:result_dict[key][x]+','+temp_dict[key][x]})
	for i in [15,17,19,21]:
		key_text = table[i][0]
		if key_text.find(",") != -1:
			keys = key_text.split(",")
		else:
			keys = [key_text]
		for key in keys:
			accent = copy.copy(key)
			key = key.encode('utf-8').replace(b'\xCC\x81',b'').decode('utf-8')
			temp_dict = {key:{'accent':accent,'tense':table[i-1][0],'part':table[0][0],'root':table[0][1]}}
			if key != "&nbsp;" and key not in result_dict:
				result_dict.update(temp_dict)
			elif key in result_dict:
				for x in result_dict[key]:
					if x not in temp_dict[key]:
						result_dict[key].update({x:result_dict[key][x]+','})							
					elif result_dict[key][x] != temp_dict[key][x]:
						result_dict[key].update({x:result_dict[key][x]+','+temp_dict[key][x]})
	for i in [11,12,13]:
		for j in range(1,len(table[i])):
			key_text = table[i][j]
			if key_text.find(",") != -1:
				keys = key_text.split(",")
			else:
				keys = [key_text]
			for key in keys:
				accent = copy.copy(key)
				key = key.encode('utf-8').replace(b'\xCC\x81',b'').decode('utf-8')
				temp_dict = {key:{'accent':accent,'tense':table[10][0],'part':table[0][0],'root':table[0][1],'plural':table[2][j]}}
				if j == 1:
					temp_dict[key].update({'gender':table[i][0]})
				if key != "&nbsp;" and key not in result_dict:
					result_dict.update(temp_dict)
				elif key in result_dict:
					for x in result_dict[key]:
						if x not in temp_dict[key]:
							result_dict[key].update({x:result_dict[key][x]+','})							
						elif result_dict[key][x] != temp_dict[key][x]:
							result_dict[key].update({x:result_dict[key][x]+','+temp_dict[key][x]})
	return result_dict

def build_dict_last_name(table):
	result_dict = {}
	root = table[0][1]
	for i in range(2,len(table)):
		for j in range(1,len(table[i])):
			key_text = table[i][j]
			if key_text.find(",") != -1:
				keys = key_text.split(",")
			else:
				keys = [key_text]
			for key in keys:
				accent = copy.copy(key)
				key = key.encode('utf-8').replace(b'\xCC\x81',b'').decode('utf-8')
				if len(key) > 4:
					if key[0:5] == "при" + root[0:2]:
						key = key[3:len(key)]
						accent = accent[3:len(accent)]				
				temp_dict = {key:{'accent':accent,'case':table[i][0],'part':table[0][0],'root':root}}
				if table[1][j] != "множина":
					temp_dict[key].update({'gender':table[1][j]})
				else:
					temp_dict[key].update({'plural':table[1][j]})
				if key != "&nbsp;" and key not in result_dict:
					result_dict.update(temp_dict)
				elif key in result_dict:
					for x in result_dict[key]:
						if x not in temp_dict[key]:
							result_dict[key].update({x:result_dict[key][x]+','})							
						elif result_dict[key][x] != temp_dict[key][x]:
							result_dict[key].update({x:result_dict[key][x]+','+temp_dict[key][x]})
	return result_dict

def build_dict_num(table):
	result_dict = {}
	root = table[0][1]
	for i in range(2,len(table)):
		for j in range(1,len(table[i])):
			key_text = table[i][j]
			if key_text.find(",") != -1:
				keys = key_text.split(",")
			else:
				keys = [key_text]
			for key in keys:
				accent = copy.copy(key)
				key = key.encode('utf-8').replace(b'\xCC\x81',b'').decode('utf-8')
				if len(key) > 4:
					if key[0:4] == "на/в" or key[0:4] == "на/у":
						key = key[4:len(key)]
						accent = accent[4:len(accent)]
					elif key[0:4] == "по" + root[0:2] or key[0:4] == "на" + root[0:2]:
						key = key[2:len(key)]
						accent = accent[2:len(accent)]
					elif key[0:5] == "уна/у":
						key = key [5:len(key)]
						accent = accent[5:len(accent)]					
				temp_dict = {key:{'accent':accent,'case':table[i][0],'part':table[0][0],'root':root}}
				if key != "&nbsp;" and key not in result_dict:
					result_dict.update(temp_dict)
				elif key in result_dict:
					for x in result_dict[key]:
						if result_dict[key][x] != temp_dict[key][x]:
							result_dict[key].update({x:result_dict[key][x]+','+temp_dict[key][x]})
	return result_dict

def build_dict_other(table):
	result_dict = {}
	key_text = table[0][1]
	if key_text.find(",") != -1:
		keys = key_text.split(",")
	else:
		keys = [key_text]
	for key in keys:
		accent = copy.copy(key)
		key = key.encode('utf-8').replace(b'\xCC\x81',b'').decode('utf-8')
		temp_dict = {key:{'accent':accent}}
		if key != "&nbsp;" and key not in result_dict:
			result_dict.update(temp_dict)
		elif key in result_dict:
			for x in result_dict[key]:
				if result_dict[key][x] != temp_dict[key][x]:
					result_dict[key].update({x:result_dict[key][x]+','+temp_dict[key][x]})
	return result_dict

def add_dict(my_dict):
	for x in my_dict:
		if x in master_dict:
			master_x_value = master_dict[x]
			my_x_value = my_dict[x]
			criteria_1 = False
			criteria_2 = False
			for y in my_x_value:
				try:
					criteria_1 = (my_x_value[y] != master_x_value[y]) or criteria_1
				except:
					criteria_2 = True
			if criteria_1 or criteria_2:
				master_dict.update({x+'2':my_dict[x]})
		else:
			master_dict.update({x:my_dict[x]})

def complete_file(new_dict,file_name):
	add_dict(new_dict)
	completed_files.append(file_name)

if __name__ == '__main__':
	for file_name in os.listdir("ignore_files/html_files"):
	#for file_name in ["html_file106210.html"]:
		if file_name[0:9] == "html_file":
			print(file_name)
			file_file = open("ignore_files/html_files/"+file_name,"r")
			file_text = file_file.read()
			file_file.close()
			file_table = generate_table(file_text)
			if file_table[0][0].find("іменник") != -1 or file_table[0][0].find("власна назва") != -1:
				new_dict = build_dict_noun(file_table)
				complete_file(new_dict,file_name)
			elif file_table[0][0].find("прикметник") != -1 or file_table[0][0].find("займенник") != -1 or file_table[0][0].find("числівник порядковий") != -1:
				new_dict = build_dict_adjective(file_table)
				complete_file(new_dict,file_name)
			elif file_table[0][0].find("дієслово недоконаного") != -1:
				new_dict = build_dict_imperf_verb(file_table)
				complete_file(new_dict,file_name)
			elif file_table[0][0].find("дієслово доконаного виду") != -1:
				new_dict = build_dict_perf_verb(file_table)
				complete_file(new_dict,file_name)
			elif file_table[0][0].find("прізвище") != -1:		
				new_dict = build_dict_last_name(file_table)
				complete_file(new_dict,file_name)
			elif file_table[0][0].find("числівник кількісний") != -1:
				new_dict = build_dict_num(file_table)
				complete_file(new_dict,file_name)
			elif file_table[0][0] == 'other':
				new_dict = build_dict_other(file_table)
				complete_file(new_dict,file_name)
	program_exit("exited successfully")








