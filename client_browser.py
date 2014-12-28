# http://avahi.org/wiki/PythonBrowseExample
import dbus, gobject, avahi
from dbus import DBusException
from dbus.mainloop.glib import DBusGMainLoop

import cPickle as pickle
from server import Server

TYPE = "_servermgr._tcp"

#Below is stuff from printer
#~ (dbus.Int32(3), dbus.Int32(0), dbus.String(u'Printer1'), dbus.String(u'ipp._tcp'), 
#~ dbus.String(u'local'), dbus.String(u'pgubuntu.local'), dbus.Int32(0), dbus.String(u'10.0.0.6'), 
#~ dbus.UInt16(4321), dbus.Array([], signature=dbus.Signature('ay')), dbus.UInt32(5L))
 
# A dictionary indexed by names
servers = {}

def service_resolved(*args):
    port = int(args[8])
    address = str(args[7])
    name = str(args[2])
    print address
    if address.find(":") == -1:
        # server[name]=[address,port]
        s = Server(name, address, port)
        if name not in servers.keys():
            servers[name] = s
            with open("server_information.pickle",'wb') as fp:
                pickle.dump(servers, fp)
        

def print_error(*args):
    print 'error_handler'
    print args[0]


def myhandler(interface, protocol, name, stype, domain, flags):
    print "Found a server manager Name: '%s' type: '%s' domain: '%s' " % (name, stype, domain)

    if flags & avahi.LOOKUP_RESULT_LOCAL:
            # local service, skip
            pass

    server.ResolveService(interface, protocol, name, stype, 
        domain, avahi.PROTO_UNSPEC, dbus.UInt32(0), 
        reply_handler=service_resolved, error_handler=print_error)

loop = DBusGMainLoop()

bus = dbus.SystemBus(mainloop=loop)

server = dbus.Interface( bus.get_object(avahi.DBUS_NAME, '/'),
        'org.freedesktop.Avahi.Server')

sbrowser = dbus.Interface(bus.get_object(avahi.DBUS_NAME,
        server.ServiceBrowserNew(avahi.IF_UNSPEC,
            avahi.PROTO_UNSPEC, TYPE, 'local', dbus.UInt32(0))),
        avahi.DBUS_INTERFACE_SERVICE_BROWSER)

sbrowser.connect_to_signal("ItemNew", myhandler)

gobject.MainLoop().run()
