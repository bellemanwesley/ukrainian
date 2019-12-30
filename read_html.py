import os
import json
import copy

letter_order = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюяа́я́е́є́и́і́ї́о́у́ю́'.encode('utf-16')
cap_letter_order = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯА́Я́Е́Є́И́І́Ї́О́У́Ю́'.encode('utf-16')
case = "відмінок"

def generate_table(file_text):
	word_type_start = file_text.find("gram_style") + 14
	word_type_stop = file_text.find("</span>",word_type_start)
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
			entryend = row.find("</td>",entrybegin)
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

def add_dict(my_dict):
	for x in my_dict:
		if not os.path.isfile('ignore_files/word_files/'+x[0]+'.json'):
			new_file = open('ignore_files/word_files/'+x[0]+'.json','w+')
			new_file.close()
		master_file = open('ignore_files/word_files/'+x[0]+'.json','r+')	
		master_text = copy.copy(master_file.read())
		if master_text == "":
			master_dict = {}
		else:
			master_dict = json.loads(master_text)
		master_file.close()
		if x in master_dict:
			master_x_value = master_dict[x]
			my_x_value = my_dict[x]
			for y in my_x_value:
				if my_x_value[y] != master_x_value[y]:
					master_dict.update({x:my_dict[x]})
		else:
			master_dict.update({x:my_dict[x]})
		master_file = open('ignore_files/word_files/'+x[0]+'.json','w+')
		master_file.write(json.dumps(master_dict,ensure_ascii=False))
		master_file.close()

if __name__ == '__main__':
	for file_name in os.listdir("html_files"):
	#for file_name in ["html_file1.html","html_file39.html"]:
		if file_name[0:9] == "html_file":
			file_text = open("html_files/"+file_name,"r").read()
			if file_text.find("іменник") != -1:
				file_table = generate_table(file_text)
				new_dict = build_dict_noun(file_table)
				add_dict(new_dict)
				file_complete = open("ignore_files/completed_html_files/"+file_name,"w+")
				file_complete.write(file_text)
				file_complete.close()
				os.remove("html_files/"+file_name)





