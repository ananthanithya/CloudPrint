import avahi
import dbus
import time
import json
import zmq
import socket
import threading
from dbus.mainloop.glib import DBusGMainLoop
import avahi
import gobject


from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

class ZeroconfBrowser:
    def __init__(self, service_type):
        self.service_browsers = set()
        self.services = {}
        self.lock = threading.Lock()
        self.service_type = service_type        
        #self.new_handler = new_handler
        #self.remove_handler = remove_handler                
        
        print "Creating variables for loop bus and server"
        loop = DBusGMainLoop(set_as_default=True)
        self._bus = dbus.SystemBus(mainloop=loop)
        self.server = dbus.Interface(
                self._bus.get_object(avahi.DBUS_NAME, avahi.DBUS_PATH_SERVER), 
                avahi.DBUS_INTERFACE_SERVER)

        print "Starting "
        thread = threading.Thread(target=gobject.MainLoop().run)
        thread.daemon = True
        thread.start()

        self.browse(service_type)
        #self.browse("_http._tcp")

    def browse(self, service):
        if service in self.service_browsers:
            return
        self.service_browsers.add(service)

        with self.lock:
            browser = dbus.Interface(self._bus.get_object(avahi.DBUS_NAME, 
            self.server.ServiceBrowserNew(avahi.IF_UNSPEC, 
                    avahi.PROTO_UNSPEC, service, 'local', dbus.UInt32(0))),
            avahi.DBUS_INTERFACE_SERVICE_BROWSER)

            browser.connect_to_signal("ItemNew", self.item_new)
            browser.connect_to_signal("ItemRemove", self.item_remove)
            browser.connect_to_signal("AllForNow", self.all_for_now)
            browser.connect_to_signal("Failure", self.failure)
            browser.connect_to_signal("ClientNew",self.client_new)

    def resolved(self, interface, protocol, name, service, domain, host, aprotocol, address, port, txt, flags):
        print "resolved", interface, protocol, name, service, domain, flags
        #self.new_handler( interface, protocol, name, service, domain, host, aprotocol, address, port, txt, flags)

    def failure(self, exception):
        print "Browse error:", exception

    def item_new(self, interface, protocol, name, stype, domain, flags):
        with self.lock:
            self.server.ResolveService(interface, protocol, name, stype,
                    domain, avahi.PROTO_UNSPEC, dbus.UInt32(0),
                    reply_handler=self.resolved, error_handler=self.resolve_error)

    def client_new(self,interface,protocol,name,stype,domain,flags):
        with self.lock:
            print "new client", interface, protocol, name, service, domain, flags
            self.register_client( interface, protocol, name, service, domain, host, aprotocol, address, port, txt, flags)
            
    def item_remove(self, interface, protocol, name, service, domain, flags):
        print "removed", interface, protocol, name, service, domain, flags
        #self.remove_handler()

    def all_for_now(self):
        print "all for now"

    def resolve_error(self, *args, **kwargs):
        with self.lock:
            print "Resolve error:", args, kwargs

