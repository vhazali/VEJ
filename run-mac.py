#! /usr/bin/python
import os
import io
import re
import subprocess

def phase1():
	# Variables
	compiled_list = {}
	location_list = {}
	apk_with_sdk = 0
	apk_without_sdk = 0

	# Retrieve all APK files into my_list
	apk_dir = "apk/"
	my_list = os.listdir(apk_dir) 

	# Retrieve SDK version of each APK file
	print("[AAPT] Retrieve SDK version of each APK file ..")
	for apk in my_list:
		apk_path = apk_dir + apk
		proc = subprocess.Popen(["./aapt", "dump", "badging", apk_path], stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate()

		sdk_byte = None
		target = False
		location_used = False
		camera_used = False

		if b'targetSdkVersion:' in out:
			index = out.find('targetSdkVersion:'.encode())
			sdk_byte = out[index+17:index+20]
			target = True
		elif b'sdkVersion:' in out:
			index = out.find('sdkVersion:'.encode())
			sdk_byte = out[index+11:index+14]
		if sdk_byte:
			sdk = str(sdk_byte, "utf-8")
			result = sdk.replace("'","")

			compiled_list[apk_path] = result
			apk_with_sdk += 1

			# Toggle True for location use
			if b"uses-feature: name='android.hardware.location" in out:
				location_used = True
				location_list[apk_path] = result
		else:
			#print("No SDK found !!")
			apk_without_sdk += 1

	print("[AAPT] APK with SDK found:", apk_with_sdk)
	print("[AAPT] APK without SDK:", apk_without_sdk)
	print("[AAPT] For APK with SDK found, using location:", len(location_list.keys()))
	print("[AAPT] Retrieve SDK version of each APK file .. Completed !!\n")

	return location_list, apk_with_sdk, apk_without_sdk

def getFileContent(file_path):
	content = None
	with open(file_path) as f:
	    content = f.read()
	f.close()
	return content

def getCategoryList(data):
	category = []
	pattern = r'\s*\(([A-Z_]*)\)'
	matches = re.findall(pattern, data)

	for match in matches:
		if match is not "":
			if match not in category:
				category.append(match)

	return category

location_list, apk_with_sdk, apk_without_sdk = phase1()

taint_directory = "sootOutput"

if not os.path.exists(taint_directory):
	os.makedirs(taint_directory)

for k, v in location_list.items():
	sdk_version = v
	apk_file = k
	apk_filename = apk_file[4:]
	sdk_file = "android-platforms\\android-" + sdk_version + "\\android.jar"
	filename = taint_directory + "/" + apk_filename + ".xml"

	# filter and compile source and sink
	source_sink_dir = "android-platforms/android-" + sdk_version + "/"
	susi_source_path = source_sink_dir + "out_CatSources.pscout"
	susi_sink_path = source_sink_dir + "out_CatSinks.pscout"

	source_data = getFileContent(susi_source_path)
	source_category = getCategoryList(source_data)
	sink_data = getFileContent(susi_sink_path)
	sink_category = getCategoryList(sink_data)

	if 'LOCATION_INFORMATION:' in source_data:
		index = source_data.find('LOCATION_INFORMATION:')
		if index:
			temp_data = source_data[index + 21:]
			break_index = temp_data.find('\n\n')
			source_data = temp_data[:break_index]
			source_data = source_data.replace("(LOCATION_INFORMATION)","-> _SOURCE_")

	# remove category header from sink data
	for category in sink_category:
		replace_text = "(" + category + ")"
		sink_data = sink_data.replace(replace_text, "-> _SINK_")
		sink_data = sink_data.replace(category + ":", "")
	
	# Compile Source and sink into single file
	single_file = open("SourcesAndSinks.txt", "w")
	single_file.write(source_data)
	single_file.write(sink_data)
	single_file.close()

	print("[Filter & Complile] Generated single SourcesAndSinks.txt for", apk_filename)

	print("[Flowdroid] Start Taint Analysis on", apk_filename)

	if os.path.isfile(sdk_file): # Continue if sdk exists
		proc = subprocess.Popen(["java", "-Xmx4g", "-cp", "soot-trunk.jar:soot-infoflow.jar:soot-infoflow-android.jar:slf4j-api-1.7.5.jar:slf4j-simple-1.7.5.jar:axml-2.0.jar", "soot.jimple.infoflow.android.TestApps.Test", apk_file, sdk_file, "--saveresults", filename], stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]
		
		if os.path.isfile(filename):
			print("[Flowdroid] Found possible source & sink for", apk_filename, ". Results saved into", filename)
		else:
			print("[Flowdroid] No source & sink found for", apk_filename, ".")
	else:
		print("[Flowdroid]", "Android SDK platform not found for", apk_filename, ". Required SDK Version", sdk_version)

	print("[Flowdroid]", apk_filename, "DONE !!")
	print()
