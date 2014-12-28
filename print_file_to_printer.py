# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
import json
import sys
import cPickle as pickle

"""
An example client. Run master_list_server first before running this.
"""
i=1
from twisted.internet import reactor, protocol

# a client protocol
id_no = None

class ListClient(protocol.Protocol):
    """Once connected, send a message, then print the result."""
    
    def connectionMade(self):
        with open("MasterPrintFile.txt", "rb") as fp:
            file_str = fp.read()
        self.transport.write(file_str)


    def dataReceived(self, data):
        print "Got a confirmation from printer"
        if data == "Print_Process_Complete":
            with open("PrintComplete_" + id_no + ".txt", "wb") as fp:
                fp.write("The print process was complete!")

    def connectionLost(self, reason):
        print "connection lost"


class ListFactory(protocol.ClientFactory):
    protocol = ListClient

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()


# this connects the protocol to a server runing on port 3000
def main():
    global id_no
    chosen_printer_name, print_job_id = sys.argv[1:]
    id_no = print_job_id
    f1 = ListFactory()
    f = open('shared_printer_information.json', 'rb')
    json_str = f.read()
    # #json_Str is a string. hence use loads()
    printers_list = json.loads(json_str)
    # # json_data is a python list
    for obj in printers_list:
        if(obj.get('name')==chosen_printer_name):
            chosen_printer_port=obj.get('port')
            chosen_printer_addr=obj.get('address')

    reactor.connectTCP(chosen_printer_addr, chosen_printer_port, f1)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()

