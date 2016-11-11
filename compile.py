#! /usr/bin/python

import os

# Variables
content_list = []
susi_sink_category = ["LOCATION_INFORMATION:", "PHONE_CONNECTION:", "VOIP:", "PHONE_STATE:", "EMAIL:", "BLUETOOTH:", "ACCOUNT_SETTINGS:", "AUDIO:", "SYNCHRONIZATION_DATA:", "NETWORK:", "FILE:", "LOG:", "SMS_MMS:", "CONTACT_INFORMATION:", "CALENDAR_INFORMATION:", "SYSTEM_SETTINGS:", "BROWSER_INFORMATION:", "NFC:", "NO_CATEGORY:"]
susi_source_path = None
susi_sink_path = None

# Get Susi generated source 
for path, subdirs, files in os.walk(r'SourceSinkLists'):
   for filename in files:
     f = os.path.join(path, filename)
     content_list.append(f)

# Extract Source and Sink path
for f in content_list:
	if f.endswith(".txt"):
		if "CatSources" in f:
			susi_source_path = f
		if "CatSinks" in f:
			susi_sink_path = f


print("Source", susi_source_path)
print("Sink", susi_sink_path)

source_data = None
with open(susi_source_path) as f:
    source_data = f.read()
f.close()

if 'LOCATION_INFORMATION:' in source_data:
	index = source_data.find('LOCATION_INFORMATION:')
	if index:
		temp_data = source_data[index + 21:]
		break_index = temp_data.find('\n\n')
		source_data = temp_data[:break_index]
		source_data = source_data.replace("(LOCATION_INFORMATION)","-> _SOURCE_")

sink_data = None
with open(susi_sink_path) as f:
    sink_data = f.read()
f.close()
 
# remove category header from sink data
for category in susi_sink_category:
	replace_text = "(" + category[:-1] + ")"
	sink_data = sink_data.replace(replace_text, "-> _SINK_")
	sink_data = sink_data.replace(category, "")

# Compile Source and sink into single file
single_file = open("SourcesAndSinks.txt", "w")
single_file.write(source_data)
single_file.write(sink_data)
single_file.close()

