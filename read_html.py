import os

sequence = 0
for x in os.listdir('html_files'):
	if x[0:4] == 'html':
		f_origin_file = open('html_files/'+x,'r')
		f_origin = f_origin_file.read()
		if f_origin.find('<span class="word_style" >а') != -1:
			f_destination = open('word_files/'+'а_'+str(sequence),'w+')
			f_destination.write(f_origin)
			sequence += 1