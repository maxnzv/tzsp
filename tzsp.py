#! /usr/bin/env python3

import socket

UDP_IP = '0.0.0.0'
UDP_PORT = 37008

sock = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)

sock.bind ((UDP_IP, UDP_PORT))

def get_mac (data, index):
    """ Converts MAC from hex to String """
    mac = format (data[index], '02x')
    for i in range (1, 6):
        mac += ':' + format (data[index+i], '02x')
    return mac

while True:
    # Listen to the stream
    data, addr = sock.recvfrom(65535)
    
    # Get packets with MAC only
    if data[3] != 18:
        continue
    next_tag = 6 + data[5]
    
    # Skip the TZSP header
    while True:
        #print (data[next_tag], data[next_tag + 1])
        if data[next_tag] == 1:
            break
        next_tag = next_tag + 2 + data[next_tag + 1]
    header_len = next_tag
    data_len = data[next_tag+1]
    data_start = header_len + 2
    if len(data) < 50:
        continue
    print ("MAC: ", get_mac(data, data_start+3), " - ", get_mac(data, data_start+9))
