# http://avahi.org/wiki/PythonBrowseExample
import dbus, gobject, avahi
from dbus import DBusException
from dbus.mainloop.glib import DBusGMainLoop
import json

import cPickle as pickle
from printer import Printer

TYPE = "_ipp._tcp"

# A dictionary indexed by names
printers = {}
i=1

# Should be called when a printer is removed
def service_lost(interface, protocol, name, stype, domain, flags):
    global i
    global printers
    print "Lost service '%s' type '%s' domain '%s' " % (name, stype, domain)    
    for key in printers:            
        if (printers[key]['name']==name):
            del printers[key]
            with open("shared_printer_information.json",'wb') as fp:
                json.dump(printers.values(), fp)
            break


def service_resolved(*args):
    global i
    global printers
    port = int(args[8])
    address = str(args[7])
    name = str(args[2])
    if address.find(":") == -1:
        # if name not in printers.keys():
        for printer_no in printers.keys():
            if name == printers[printer_no]['name']:
                return
        printers[i]={"name":name,"address":address,"port":port}
        with open("shared_printer_information.json", 'wb') as fp:
            json.dump(printers.values(),fp)
            i=i+1
        

def print_error(*args):
    print 'error_handler'
    print args

def myhandler(interface, protocol, name, stype, domain, flags):
    print "Found service '%s' type '%s' domain '%s' " % (name, stype, domain)

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
sbrowser.connect_to_signal("ItemRemove", service_lost)

gobject.MainLoop().run()
