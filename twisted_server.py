
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

import json
from twisted.internet import reactor, protocol


class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""
    
    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        if (data == "printer_list"):
            f = open('shared_printer_information.json', 'rb')
            json_data=f.read()
            # print json_data+"\n\n"
            # json_data  = json.load(open("shared_printer_information.json"))
            # json_str=json.loads(json_data)
            # print json_str
            self.transport.write(json_data)
        else:
            self.transport.write("It didn't read from file!")


def main():
    """This runs the protocol on port 8000"""
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(8000,factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()