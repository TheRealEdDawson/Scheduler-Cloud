from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.storage.drivers.atmos import AtmosError
import libcloud.security
import string
import os
import datetime
import time
import sys
import logging

# Checking that all the arguments were entered on the command line, exiting with a message if not.
if len(sys.argv) < 5:
    argumentsnotset = '\nError: one or more arguments were not passed. \n\nUsage is like so: \n\nPython Scheduler-Cloud.py api-key.txt secret-key.txt config-file.txt datestamp=off'
    print argumentsnotset
    sys.exit(1)	

#Processing command line arguments for use

# Processing text file to retrieve api key
api_key_file = open(sys.argv[1])
for line in api_key_file:
    api_key = line.rstrip()
api_key_file.close()
#print 'API KEY = ', api_key

# Processing text file to retrieve secret key
secret_key_file = open(sys.argv[2]) 
for line in secret_key_file:
    secret_key = line.rstrip()
secret_key_file.close()
#print 'Secret Key = ', secret_key

# Processing text file to retrieve user's configuration settings
config_file_contents = ""
print 'Processing string for config_file: ' + sys.argv[3]
config_file = open(sys.argv[3]) 
for line in config_file:
    config_file_contents = line.rstrip()
config_file.close()
#Check that config file has something in it 
if config_file_contents == "":
    print "ERROR: Config File is Empty!"
    sys.exit(1)	
print "\nConfig File Contents are: ", config_file_contents, "\n"

# Processing text command line to switch datestamping on or off
loggydatestamp = datetime.date.today().strftime("%d-%B-%Y")
date_stamp_toggle = sys.argv[4]
if (date_stamp_toggle == "datestamp=on"):
    rootstring="O"
    print 'Datestamping is ON'
    datestamp = datetime.date.today().strftime("%d-%B-%Y")
    #print datestamp
    container_name = (datestamp)
else:
    print 'Datestamping is OFF'
    rootstring=''
    datestamp=''
    container_name = ('')

# Set up logging file
logfilename = loggydatestamp + '-Scheduler-Cloud' + '.log'
print 'Logging to ' + logfilename
logging.basicConfig(filename=logfilename,filemode='w',level=logging.INFO,format='%(asctime)s %(message)s')
initialloggystring = 'New scan started.' + loggydatestamp
print initialloggystring
logging.info(initialloggystring)
errorcount = 0

#Logging in and verifying credentials
print '\nLogging in...'
#Security Block -- Logging in with our certificates
libcloud.security.VERIFY_SSL_CERT = False
Ninefold = get_driver(Provider.NINEFOLD)
conn = Ninefold(api_key, secret_key)
# This plays out as driver = Ninefold('YOUR Ninefold API Key HERE', 'YOUR Ninefold Secret Key HERE')

#def showinstances():
# Show a list of the currently running instances
nodes = conn.list_nodes()
statusloggystring = "Running instances: ", nodes
print "\n", statusloggystring
logging.info(statusloggystring)
#return nodes

#def showimages():
# Show a list of the available VM images 
images = conn.list_images()
statusloggystring = "Available images: ", images
print "\n", statusloggystring
logging.info(statusloggystring)
#return images

#def showsizes():
# Show a list of the available VM sizes
sizes = conn.list_sizes()
statusloggystring = "Available sizes: ", sizes
print "\n", statusloggystring
logging.info(statusloggystring)
#return sizes

#def configactions(config_file_contents, loggydatestamp):
# Take action based on the config file commands
# for line in config_file_contents:
if config_file_contents == "create_tiny":
    servername = ("Test" + loggydatestamp)
    node = conn.create_node(name=servername, image=images[1], size=sizes[0])
    statusloggystring = "Instance created: ", servername
    print "\n", statusloggystring
    logging.info(statusloggystring)

# Main Program Block
#showinstances()
#showimages()
#showsizes()
#configactions(config_file_contents, images, sizes, loggydatestamp)
#showinstances()

endloggystring = "\n*** END PROCESS ***\n"
logging.info(endloggystring)

print 'Process complete. ', errorcount, ' error(s) were found. \nSee the logfile: ', logfilename, ' for details.'
