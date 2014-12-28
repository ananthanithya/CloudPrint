class Printer():
    def __init__(self, printer_name, address, port, location=None):
        self.printer_name = printer_name
        self.location = location
        self.address = address
        self.port = port

