#!/usr/bin/python
import socketserver
import _thread
import time
import binascii
import sys

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

def redsea (srv):
    import os
    #os.system ("nc -l -u 12345 | redsea -x -p | nc -u 127.0.0.1 52005")
    while True:
        #os.system ("nc -l -u 12345 | redsea -x -p | nc -u 127.0.0.1 52005")
        os.system ("/home/sjg/git/gr-scripts/sdr_to_xdr/run-redsea.sh")
        print ("buf reconn")

def rds(srv):
    import socket

    UDP_IP = "127.0.0.1"
    UDP_PORT = 52005

    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP

    sock.bind((UDP_IP, UDP_PORT))

    while True:
        out, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        data = str(out, 'utf-8')
        data = data.replace (" ", "")

        if len(data) == 17:
            if data[0:4] != "----":
                srv.sendall("P" + data[0:4])
                #print ("P" + data[0:4])

            err = 0
            if data[4:8] == "----":
                err |= 3
            if data[8:12] == "----":
                err |= 12
            if data[12:16] == "----":
                err |= 48

            err_str = "%0.2X" % err
            data = data.replace ("-", "0")
            msg = "R" + data[4:16] + err_str + "\n"
            srv.sendall(msg)
        else:
            print ("invalid msg:", data)

def main(top_block_cls=fmdx_sdr, options=None):
    tb = fmdx_sdr ()

    socketserver.TCPServer.allow_reuse_address = True
    server = XDRServer(('0.0.0.0', 7373), XDRHandler, tb, password="kornerowopuotzk-x", allow_guests=True)
    _thread.start_new_thread(server.serve_forever, ())
    _thread.start_new_thread(poll,(tb,server,))
    _thread.start_new_thread(redsea,(server,))
    _thread.start_new_thread(rds,(server,))

    tb.start()
    tb.wait()

if __name__ == "__main__":
    import ctypes
    import sys
    main()
