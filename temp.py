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
index = 25915
status = 0
while index < 45485:
	s3.download_file('ukrainian-words', 'm9html/html_file'+str(index)+'.html', 'ignore_files/html_files/m9html_file'+str(index)+'.html')
	index += 1
	if status != int(100*index/45485.0):
		status = int(100*index/45485.0)
		print(status)
#'''