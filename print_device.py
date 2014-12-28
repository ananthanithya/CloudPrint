import publish_service
import time
import sys
import os

printer_name, printer_port = sys.argv[1:]

def service_manager_publisher():
    service = publish_service.ZeroconfService(name=printer_name, port=printer_port, stype="_ipp._tcp")
    service.publish()

print "Publishing myself ("+printer_name+") as a printer service on Zeroconf, on port "+printer_port
service_manager_publisher()

print "Listening for incoming print requests"
os.system("python print_process.py " + str(printer_name) + "   " + str(printer_port) + " &")

while True:
    time.sleep(1)

