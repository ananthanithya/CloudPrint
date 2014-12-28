import avahi
import dbus
import time
import json
import zmq
import socket
import cPickle as pickle
import os

#import publish_service

from printer import Printer

import threading
from dbus.mainloop.glib import DBusGMainLoop
import avahi
import gobject

from browser import ZeroconfBrowser
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import publish_service

def service_manager_publisher():
    service = publish_service.ZeroconfService(name="PrintService", port=3000)
    print "Publishing service name: PrintService on port: 3000"
    service.publish()

service_manager_publisher()


os.system("python master_list_server.py &")

while True:
    time.sleep(1)
