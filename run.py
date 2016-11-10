#! /usr/bin/python
import os
import io
import subprocess

# Variables
compiled_list = {}
camera_list = {}
location_list = {}
both_list = {}
apk_with_sdk = 0
apk_without_sdk = 0

# Retrieve all APK files into my_list
my_list = os.listdir("apk/") 

# Retrieve SDK version of each APK file
print("Retrieve SDK version of each APK file ..\n")
for apk in my_list:
	apk_path = "apk/"+ apk
	#os.system("aapt dump badging apk/" + apk + "|FINDSTR Version")
	proc = subprocess.Popen(["aapt", "dump", "badging", apk_path], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	#out = proc.stdout.read()

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
		'''
		if target:
			print("using target SDK:",result)
		else:
			print("using minimum SDK:",result)
		'''
		compiled_list[apk_path] = result
		apk_with_sdk += 1

		# Toggle True for location use
		if b"uses-feature: name='android.hardware.location" in out:
			location_used = True
			location_list[apk_path] = result
		
		# Toggle True for camera use
		if b"uses-feature: name='android.hardware.camera" in out:
			camera_used = True
			camera_list[apk_path] = result

		if camera_used and location_used:
			both_list[apk_path] = result
	else:
		#print("No SDK found !!")
		apk_without_sdk += 1

	'''
	# Toggle True for location use
	if b"uses-feature: name='android.hardware.location" in out:
		location_used = True
		location_list[apk_path] = result
	
	# Toggle True for camera use
	if b"uses-feature: name='android.hardware.camera" in out:
		camera_used = True
		camera_list[apk_path] = result

	if camera_used and location_used:
		both_list[apk_path] = result
	'''

print("[Android SDK] APK with SDK found:", apk_with_sdk)
print("[Android SDK] APK without SDK:", apk_without_sdk)
print("[Android SDK] For APK with SDK found, using location:", len(location_list.keys()))
print("[Android SDK] For APK with SDK found, APK using camera:", len(camera_list.keys()))
print("[Android SDK] For APK with SDK found, APK using both:", len(both_list.keys()), "\n")
print("Retrieve SDK version of each APK file .. Completed !!\n")

print("Print list of apk with sdk version ..\n")
print("SDK\tAPK file")
for k, v in compiled_list.items():
	print(v, "\t", k)

print("\n")
print("Implement SuSi for each apk to get Source and Sink ..")
'''
Susi commands here
'''

print("\n")
print("Modify each Source & Sink for flowdroid ..")
'''
Extract location and camera source
Modify and combine output source and sink file into SourcesAndSinks.txt
'''

print("\n")
print("Run flowdroid ..")
'''
Flowdroid commands here
'''
directory = "sootOutput"

if not os.path.exists(directory):
	os.makedirs(directory)

for k, v in compiled_list.items():

	apk_filepath = k
	apk_filename = apk_filepath[4:]
	sdk_file = "android-platforms\\android-" + str(v) + "\\android.jar"
	filename = directory + "/" + apk_filename + ".xml"

	if os.path.isfile(sdk_file): # Continue if sdk exists

		proc = subprocess.Popen(["java", "-Xmx4g", "-cp", "soot-trunk.jar;soot-infoflow.jar;soot-infoflow-android.jar;slf4j-api-1.7.5.jar;slf4j-simple-1.7.5.jar;axml-2.0.jar", "soot.jimple.infoflow.android.TestApps.Test", apk_filepath, sdk_file, "--saveresults", filename], stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]
		#(out, err) = proc.communicate()
		#out = proc.stdout.read()
		if os.path.isfile(filename):
			print("[Flowdroid] Found possible source & sink for", apk_filename, ". Results saved into", filename)
		else:
			print("[Flowdroid] No source & sink found for", apk_filename, ".")
	else:
		print("[Flowdroid]", "Andoird SDK platform not found for", apk_filename, ". Required SDK Version", str(v))

	print("[Flowdroid]", k, "DONE !!")