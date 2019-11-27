import subprocess # to call lsluns

# --DUCK--

# Decode the bytestream given to us by the
# subprocess call to from ascii to unicode
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

# Create a new function to scan for free LUN's and
# accompanying FCP devices.
def scanFCP(rh):
	"""
	Scan the SAN Fabric for LUN's that are free to image.

	Input:
		Request Handle

	OutPut:
		This function will update the database with free
		FCP/WWPN/LUN triplets available for deploying new
		Linux guests.

	"""
	
	rh.printSyslog("Enter scanFCP function")

	# Scan for LUN's on the SAN network
	if subprocess.call("lszfcp") != 0:
		rh.results["overallRC"] = 3
		rh.printSysLog("No FCP devices attached: " +
			str(rh.results["overallRC"]))
	else:
		scan_ouput = subprocess.check_output(["lsluns"])
		if not scan_output:	# Cannot scan for luns failure
			rh.results["overallRC"] = 3	# Return non-zero return code (exit with failure)
			rh.printSysLog("Failed to scan for LUN's on the SAN fabric: " +
				str(rh.results["overallRC"]))
		else:
			scan_output = concatenate(scan_output) # decode output to unicode
			for line in scan_output:
				if "port" in line:
					wwpns = line.split('0x')[1].strip(':')
