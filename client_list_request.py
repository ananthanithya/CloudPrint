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

class ListClient(protocol.Protocol):
    """Once connected, send a message, then print the result."""
    
    def connectionMade(self):
        # global i
        # if(i==1):
        self.transport.write("printer_list")
            # i=i+1
        # else:
        #     self.transport.write("###Incoming file:"+user_choice_json)
    
    def dataReceived(self, data):
       # print "Printing the data received by client list request " + str(data)
        if data == "Print_Process_Complete":
            print "The print is complete. You can go collect the print job!"
        else:
            "As soon as any data is received, write it back."
            # data is a string. hence use loads()
          #  print "Data in client list request is" + data
            json_data=json.loads(data)
            # json_data is a python list
            print "Available printers:\n"
            for obj in json_data:
               print obj.get('name')
            printer_name=raw_input('Enter a printer name\n')
            file_path=raw_input('Enter file path to be printed\n')
            with open(file_path,'r') as fp:
                file_contents=fp.read();
          #  print "file_contents",file_contents
            user_choice= {"contents":file_contents,"printer_name":printer_name}
         #   print "user_choice",user_choice
            user_choice_json  = json.dumps(user_choice)
        #    print "user_choice_json",user_choice_json
            self.transport.write("Incoming file:"+user_choice_json)
    
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
    
    f = ListFactory()
    with open('server_information.pickle', 'rb') as fp:
        servers = pickle.load(fp)
    address = servers[servers.keys()[0]].address
    port    = servers[servers.keys()[0]].port
    #print address
    #print port
    reactor.connectTCP(address, port, f)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
