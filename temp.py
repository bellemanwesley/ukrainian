import os
import json
import re

text_file = open("ignore_files/test_page.txt","r")
text = text_file.read()
text_file.close()
paragraph_list = re.split(r"\s*\n+\s*",text)

#text_list = re.split(r"\s+",text)

#print(text_list)

'''
request_dict = {"key":"accent"}
for i in range(len(text_list)):
	request_dict.update({str(i+1):text_list[i]})

request_json = json.dumps(request_dict)
request_json = request_json.replace("\"","\\\"")
response = os.popen("curl http://localhost:5000/deploy -X POST -H \"Content-Type: application/json\" -d \""+request_json+"\"").read()
response_dict = json.loads(response)

for x in response_dict:
	dict_bin = bytes(response_dict[x],encoding='utf-16')
	response_dict[x] = dict_bin.decode('utf-16')

result = ''
for i in range(len(response_dict)-1):
	result = result + response_dict[str(i+1)] + ' '

print(result)'''