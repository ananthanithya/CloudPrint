CloudPrint
==========

This project proposes to solve the problem of providing printing as a service over the network. The Avahi daemon, running the Zeroconf protocol, is used as a discovery service between the cloud server, clients and printers. The printer registers itself with the print server, and periodically updates load and location information. Clients submit print jobs to the cloud print server, which returns a list of twenty-five geographically close printers available in the network, sorted according to their workload. The user then selects the printer and submits the job. Information on the progress of the print request is
displayed on the client’s print queue.

Avahi is the Zeroconf implementation for Linux which provides us with an API for integration of mDNS/DNS-SD features into our programs. With the help of Avahi we can publish and discover services and hosts running on a local network. 
