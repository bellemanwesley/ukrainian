import os

letter_order = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
cap_letter_order = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"

low_sequence = 0
cap_sequence = 0
for x in os.listdir('html_files'):
	if x[0:4] == 'html':
		f_origin_file = open('html_files/'+x,'r')
		f_origin = f_origin_file.read()
		if f_origin.find('<span class="word_style" >б') != -1:
			f_destination = open('word_files/б/'+'б_'+str(low_sequence),'w+')
			f_destination.write(f_origin)
			low_sequence += 1
		if f_origin.find('<span class="word_style" >Б') != -1:
			f_destination = open('word_files/б/'+'cap_б_'+str(cap_sequence),'w+')
			f_destination.write(f_origin)
			cap_sequence += 1