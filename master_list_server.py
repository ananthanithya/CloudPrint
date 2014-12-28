
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

import json
from twisted.internet import reactor, protocol

from twisted.internet import stdio, reactor, protocol
from twisted.protocols import basic
import re
import os
import time

print_job_id = 1

## when client receives data from server // the client script checks then blits ##

class DataForwardingProtocol(protocol.Protocol):
    def __init__(self):
        self.output = None
        self.normalizeNewlines = False

    def dataReceived(self,data):
        if self.normalizeNewlines:

    ## see if data is == to secret ##
    ## this never returns True ? ##
            if data == 'secret':
                print "This line isn't secure"
            else:
                data = re.sub(r"(\r\n|\n)","\r\n",data)
        if self.output:
            if data == "secret":
                print "This line isn't secure"
            else:

         ## this will return the error message below ##
         ## so I'm very unsure of what is going on with 'data' ##
                self.output.write(type(data))

class StdioProxyProtocol(DataForwardingProtocol):
    def connectionMade(self):
        inputForwarder = DataForwardingProtocol()
        inputForwarder.output = self.transport
        inputForwarder.normalizeNewlines = True
        stdioWrapper = stdio.StandardIO(inputForwarder)
        self.output = stdioWrapper

class StdioProxyFactory(protocol.ClientFactory):
    protocol = StdioProxyProtocol



class List(protocol.Protocol):
    
    def dataReceived(self, data):
        "As soon as any data is received, write it backself."
        # print "Data here", data
        # strings = data.split("###")
        # print "size: ", len(strings)
        # for strg in strings:
        #     print "Strg:" , strg
            # if strg is not '' and strg.find("printer"):
        global print_job_id
       # print "Data initially " + str(data)
      #  print str(data.find("Incoming file:"))
        if(data=="printer_list"):
          #  print "inside printerlist"
            f = open('shared_printer_information.json', 'rb')
            json_str=f.read()
            # print json_data+"\n\n"
            # json_data  = json.load(open("shared_printer_information.json"))
            # print json_data
            # json_str=json.loads(json_data)
         #   print "File info:"
          #  print json_str
            self.transport.write(json_str)
        elif data.find("Incoming file:") != -1:
            #Extracting chosen printer
            user_choice_str=data[len("Incoming file:"):]
          #  print "Data:",data
            #~ print "user_choice_str:",user_choice_str           
            user_choice_json=json.loads(user_choice_str)
            chosen_printer_name = user_choice_json.get('printer_name')

            # To find port of the chosen printer
            f = open('shared_printer_information.json', 'rb')
            json_str=f.read()
            # #json_Str is a string. hence use loads()
            printers_list=json.loads(json_str)
            # # json_data is a python list
            for obj in printers_list:
                if(obj.get('name')==chosen_printer_name):
                    chosen_printer_port=obj.get('port')
                    chosen_printer_addr=obj.get('address')
            
            # Connect to the chosen printer
            with open("MasterPrintFile.txt", "w") as fp:
                fp.write(user_choice_json.get('contents'))

            os.system("python print_file_to_printer.py " + str(chosen_printer_name) + "    " + str(print_job_id) + "  & ")
            
            while not os.path.exists("PrintComplete_" + str(print_job_id) + ".txt"):
                time.sleep(0.1)
            
            print "Sending the notification that the print process is complete to Client"
            self.transport.write("Print_Process_Complete")
            os.unlink("PrintComplete_" + str(print_job_id) + ".txt")
            
            print_job_id += 1
            
            
            #~ reactor.connectTCP(chosen_printer_addr, chosen_printer_port, StdioProxyFactory())
            #~ self.transport.write(str(user_choice_json.get('contents')))
        else:
            self.transport.write("It didn't read from file!")


def main():
    """This runs the protocol on port 3000"""
    factory = protocol.ServerFactory()
    factory.protocol = List
    reactor.listenTCP(3000, factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
