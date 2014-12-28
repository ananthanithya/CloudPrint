# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

import json
from twisted.internet import reactor, protocol
import sys

global_counter = 1

printer_name, printer_port = sys.argv[1:]

class List(protocol.Protocol):
    
    def dataReceived(self, data):
        global global_counter
        global printer_name
        print "Received a file to be printed"
        print "Printing the file: Printed_File_"  + str(printer_name) + "_" + str(global_counter) + ".txt"
        with open("Printed_File_"  + str(printer_name) + "_" + str(global_counter) + ".txt", "w") as fp:
            fp.write(data)
            global_counter += 1
        print "Print process complete!"
        self.transport.write("Print_Process_Complete")

factory = protocol.ServerFactory()
factory.protocol = List
reactor.listenTCP(int(printer_port), factory)
reactor.run()
