#!/usr/bin/python
import socketserver
import _thread
import time
import binascii

from xdrserver import XDRServer
from xdrhandler import XDRHandler
from fmdx_sdr import fmdx_sdr

def poll(tb,srv):
    while True:
        rssi = tb.get_rssi_var()+tb.get_rssi_ref()
        pilot = tb.get_pilot_var()

        if pilot >= 2.5:
            st = "s"
        else:
            st = "m"

        if(srv.get_tuner_forced_mono()):
            st = st.upper()

        srv.sendall("S"+st+str(rssi))
        time.sleep(1.0 / (15))

def rds(srv):
    import socket

    UDP_IP = "127.0.0.1"
    UDP_PORT = 52001

    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        str, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        data = bytearray(str)
        if len(data)==12:
            srv.sendall("P"+binascii.hexlify(data[0:2]).upper().decode('ascii'))
            srv.sendall("R"+binascii.hexlify(data[2:8]).upper().decode('ascii')+"00")
        else:
            print ("invalid msg:", data)

def main(top_block_cls=fmdx_sdr, options=None):
    tb = fmdx_sdr ()

    socketserver.TCPServer.allow_reuse_address = True
    server = XDRServer(('0.0.0.0', 7373), XDRHandler, tb, password="password", allow_guests=True)
    _thread.start_new_thread(server.serve_forever, ())

    _thread.start_new_thread(poll,(tb,server,))
    _thread.start_new_thread(rds,(server,))

    tb.start()
    tb.wait()

if __name__ == "__main__":
    import ctypes
    import sys
    main()
