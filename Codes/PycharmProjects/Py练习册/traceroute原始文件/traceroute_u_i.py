#!/usr/bin/env python3
"""
Uses ICMP Echo Request to ping a host, or trace the hops to a host.
"""
'''add the version of udp traceroute'''
import os
import sys
import socket
import struct
import select
import time
import argparse


def udp_traceroute(dest, count=3, timeout=1):
    dest_addr = socket.gethostbyname(dest)
    port = 55285
    max_hops = 30
    ttl = 1

    try:
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        rec_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
       # timeout_Pack = struct.pack("q", timeout)  # see  socket of python  about why use struct.pack()
        # timeout 这里设成了多少? 8个字节. 用q 代表long long 同样为8个字节
        #rec_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout_Pack)
       #  rec_socket.bind(("", port))  why?
    except socket.error as msg:
        print('Socket error: %s' % msg)
        exit(1)

    print('traceroute to %s (%s), %d hops max' % (dest, dest_addr, max_hops))
    id = os.getpid() & 0xffff     #identifier 标识符

    for ttl in range(1,max_hops):
        try:
            send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
            total_rtt = []
            for j in range(count):
                send_socket.sendto(''.encode(), (dest_addr, port))
                rtt, hop_addr = recv_ping(rec_socket, dest_addr, id, timeout)
                total_rtt.append(rtt)

        except socket.error as msg:
            print('Socket error: %s' % msg)
            exit(1)

        try:
            # Try to get the hostname from the returned ip
            hop = socket.gethostbyaddr(hop_addr)[0]
        except:
            hop = hop_addr

        print('%s (%s)  ' % (hop, hop_addr), end='')

        for t in total_rtt:
            if t is None:
                print('\t*', end='', flush=True)
            else:
                print('\t%0.4f ms' % (t * 1000), end='', flush=True)
        print('\n', end='', flush=True)
        if hop_addr == dest_addr:
            break



def checksum(data):
    """
    Calculate the 16 bit checksum for data

    """
    total = 0
    # Sum 16 bits chunks (the first byte * 256 + second byte)
    for i in range(len(data) - (len(data) % 2)):
        total += (data[i] << 8) if i % 2 else data[i]

    # Add in any remaining bits
    if len(data) % 2 != 0:
        total + data[-1]

    # Add in carry bits
    total = (total & 0xffff) + (total >> 16)
    total = total + (total >> 16)

    # Flip and change order
    total = ~total & 0xffff
    return total >> 8 | (total << 8 & 0xff00)

    # Flip
    # return (~total) & 0xffff

def send_ping(icmp_socket, dest_addr, id, seq):
    """Send a single ICMP Echo Request (Control message 8, code 0)"""
    # Zero out checksum to build header
    cs = 0

    # Header: type 8, code 8, checksum 16, identifier 16, sequence 16
    # Use calculate header + data in order to calculate checksum
    header = struct.pack('BBHHH', 8, 0, cs, id, seq)

    # Add start time to calculate RTT
    data = struct.pack('d', time.time())

    # Calculate checksum and repack header with the correct checksum
    cs = checksum(header + data)
    header = struct.pack('BBHHH', 8, 0, socket.htons(cs), id, seq)
    packet = header + data

    # Make it so
    icmp_socket.sendto(packet, (dest_addr, 1))


def recv_ping(icmp_socket, dest_addr, id, timeout):
    """Receive a single ICMP packet"""
    while True:
        start_time = time.time()
        ready = select.select([icmp_socket], [], [], timeout)
        time_in_select = (time.time() - start_time)
        # time_in_select为 在select中停留的时间. 一开始为timeout.
        # 收到一次包,timeout减少一次. timeout -= time_in_select

        if ready[0] == []:
            # Timeout
            return None, None

        packet, addr = icmp_socket.recvfrom(1024)
        time_received = time.time()

        #ip数据包 从0开始数嘛.
        icmp_header = packet[20:28]
        type, code, checksum, packet_id, seq = struct.unpack('BBHHH', icmp_header)
        if addr[0] == dest_addr:
            # Unpack our the start_time we sent in the original packet
            size_of_double = struct.calcsize('d')
            time_sent = struct.unpack('d', packet[28:28 + size_of_double])[0]
            rtt = time_received - time_sent
            return rtt, addr[0]
        elif type == 11:  # Time exceeded message (TTL)
            # If we're using traceroute, calculate the start time ourselves since it wont be sent back
            rtt = time_received - start_time
            return rtt, addr[0]

        timeout -= time_in_select


def icmp_traceroute(dest, count=3, timeout=1, hops=64):
    """Trace the route to the destination using ICMP Echo Requests and limiting IP TTL to get each router to send us a Time Exceeded response"""
    ''' 做一些准备工作'''
    try:
        icmp_proto = socket.getprotobyname('icmp')
        icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp_proto) #原始套接字
        dest_addr = socket.gethostbyname(dest)
    except socket.error as msg:
        print('Socket error: %s' % msg)
        exit(1)

    id = os.getpid() & 0xffff

    hop_addr = ''
    hop = ''
    print('traceroute to %s (%s), %d hops max' % (dest, dest_addr, hops))
    # Increment the IP TTL (starting at 1) to systematically receive Time Exceeded responses from each hop
    for i in range(1, hops):
        try:
            # Set IP TTL
            icmp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, i)
            # Used to collect RTT from each hop
            total_rtt = []
            for j in range(count):
                send_ping(icmp_socket, dest_addr, id, i)
                rtt, hop_addr = recv_ping(icmp_socket, dest_addr, id, timeout)
                total_rtt.append(rtt)
        except socket.error as msg:
            print('Socket error: %s' % msg)
            exit(1)

        try:
            # Try to get the hostname from the responder
            hop = socket.gethostbyaddr(hop_addr)[0]
        except:
            hop = hop_addr

        print('%s (%s)  ' % (hop, hop_addr), end='')
        for t in total_rtt:
            if t is None:
                print('\t*', end='', flush=True)
            else:
                print('\t%0.4f ms' % (t * 1000), end='', flush=True)
        print('\n', end='', flush=True)
        if hop_addr == dest_addr:
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="An ICMP ping/traceroute and udp traceroute utility. Requires root authority ")

    parser.add_argument("destination", help="The ip address or hostname of the destination.")
    parser.add_argument("-c","--count", help="Count of  packets to be sent to the destination. The defaults is 3.",
                        type=int, default=3)
    parser.add_argument("-t","--timeout", help="Timeout in seconds. The default is 1 second.", type=int, default=1)

    parser.add_argument("-I","--icmp", help="Send Icmp packet", action="store_true")
    parser.add_argument("-U","--udp",help="Send Udp packet", action="store_true")
    parser.add_argument("--traceroute", help="Trace hops to the destination.", action="store_true")

    '''-c  -t  -I  -U'''
    args = parser.parse_args()

    if args.traceroute and args.icmp:
        icmp_traceroute(args.destination, args.count, args.timeout)

    elif args.traceroute and args.udp:
       # ping(args.destination, args.count, args.timeout)
        udp_traceroute(args.destination, args.count, args.timeout)