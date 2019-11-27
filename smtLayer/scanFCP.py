#!/usr/bin/env python

import subprocess # to call lsluns

# --DUCK--
# Create a new function to scan for free LUN's and
# accompanying FCP devices.
# THIS IS THE TEST VERSION!!!

# decode ascii stream to unicode 
# for python interpreter to work with
def concatenate(stream):
	output = []
	line = ""

	for byte in stream.decode():
		if byte != '\n':
			line += byte
		else:
			output.append(line)
			line = ""
	return output

#def scanFCP(rh):
def scanFCP():
	"""
	Scan the SAN Fabric for LUN's that are free to image.

	Input:
		Request Handle

	OutPut:
		This function will update the database with free
		FCP/WWPN/LUN triplets available for deploying new
		Linux guests.

	"""
	fcps = []		# FCP channels
	wwpns = []		# Worldwide Port Names
	lun_ids = []	# Logical Unit Numbers
	
	# Scan for LUN's on the SAN network
	if subprocess.call("lszfcp") != 0:
		print "No FCP devices attached"
		exit(-1)
	else:
#		f = open("lsluns.output", 'r')
#		scan_output = f.readlines() # read contents of file line by line.
		scan_output = subprocess.check_output(["lsluns"])
		if not scan_output:
			print "Failed to scan for LUN's on the SAN fabric"
			exit(-1)

		scan_output = concatenate(scan_output) # decode the output stream
		for line in scan_output:
			if "Scan" in line:
				fcps.append(line.split("0.0.")[1])
				continue
			elif "Unable to send the REPORT_LUNS command to LUN." in line:
				print("[DEBUG]: No LUN's found on this wwpn.")
				continue
			elif "port" in line:
				wwpn = line.split("0x")[1].strip(':\n')
				print "[DEBUG]: wwpn found 0x%s" % wwpn
				wwpns.append("0x" + wwpn)
			else:
				lun = line.split("0x")[1].strip('\n')
				lun_ids.append("0x" + lun)

	print("FCP Devices: ")
	for fcp in fcps:
		print fcp

	print("Worldwide Port Numbers: ")
	for wwpn in wwpns:
		print wwpn

	print("Logical Unit Numbers: ")
	for lun in lun_ids:
		print lun

	print "[+] DONE!"

# this function declaration is just for testing purposes
if __name__ == "__main__":
	scanFCP()
