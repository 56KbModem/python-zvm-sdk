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
   
    fcp_channels = {}

    # use strings as keys for multi-dimensional dict
    last_fcp = ""
    last_wwpn = ""
 
    # Scan for LUN's on the SAN network
    if subprocess.call("lszfcp") != 0:
        print "No FCP devices attached"
        exit(-1)
    else:
#        f = open("lsluns.output", 'r')
#        scan_output = f.readlines() # read contents of file line by line.
        scan_output = subprocess.check_output(["lsluns"])
        if not scan_output:
            print "Failed to scan for LUN's on the SAN fabric"
            exit(-1)

        scan_output = concatenate(scan_output) # decode the output stream
        for line in scan_output:
            if "Unable" in line: # scan has failed on this adapter
                continue
            elif "Scan" in line:
                last_fcp = line.split("0.0.")[1].strip('\n') # parse the line to find fcp adapter
                fcp_channels[last_fcp] = {}
            elif "port" in line:
                last_wwpn = line.split("0x")[1].strip(':\n')
                last_wwpn = "0x" + last_wwpn # make string whole again
                fcp_channels[last_fcp][last_wwpn] = []
            else:
                lun = line.split("0x")[1].strip('\n')
                lun = "0x" + lun # recreate true string

                if int(lun, 16) is not 0: # LUN ID 0x0000... should be omitted
                    fcp_channels[last_fcp][last_wwpn].append(lun) # finally write this lun to our datastructure

    for key in fcp_channels:
		print("FCP DEVICE: %s" % key)
		for subkey in fcp_channels[key]:
			print("WWPN: %s" % subkey)
			for lun_id in fcp_channels[key][subkey]:
				print("LUN ID: %s" % lun_id)

# this function declaration is just for testing purposes
if __name__ == "__main__":
    scanFCP()
