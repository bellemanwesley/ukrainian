'''
np_file = open('ignore_files/not_processed.txt','r')
np = np_file.readlines()
np_file.close()
print(len(np))

'''
#'''

import boto3
import os

s3 = boto3.client('s3')
index = 5350
status = 0
while index < 11877:
	s3.download_file('ukrainian-words', 'm7html/html_file'+str(index)+'.html', 'ignore_files/html_files/m7html_file'+str(index)+'.html')
	index += 1
	if status != int(100*index/11877.0):
		status = int(100*index/11877.0)
		print(status)
#'''