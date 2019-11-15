import

# --DUCK--
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


