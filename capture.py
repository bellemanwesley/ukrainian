import os

try:
	os.remove('sentrequests.pcap')
except:
	pass

os.system("wireshark -i en0 -f 'host lcorp.ulif.org.ua and port 80' -k -w sentrequests.pcap -a duration:5")
