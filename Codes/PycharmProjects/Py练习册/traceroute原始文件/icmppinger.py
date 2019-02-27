# NOTE THIS WILL ONLY WORK WITH SUDO ROOT e.g. sudo python icmppinger.py
# work in linux
import socket
import os
import sys
import struct
import time
import select
import binascii

label = '*************{0}*************'

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2


# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise



def checksum(data):
    """Creates the ICMP checksum as in RFC 1071
    :param data: Data to calculate the checksum ofs
    :type data: bytes
    :return: Calculated checksum
    :rtype: int
    Divides the data in 16-bits chunks, then make their 1's complement sum"""
    subtotal = 0
    for i in range(0, len(data)-1, 2):
        subtotal += ((data[i] << 8) + data[i+1])                # Sum 16 bits chunks together
    if len(data) % 2:                                           # If length is odd
        subtotal += (data[len(data)-1] << 8)                    # Sum the last byte plus one empty byte of padding
    while subtotal >> 16:                                       # Add carry on the right until fits in 16 bits
        subtotal = (subtotal & 0xFFFF) + (subtotal >> 16)
    check = ~subtotal                                           # Performs the one complement
    return ((check << 8) & 0xFF00) | ((check >> 8) & 0x00FF)    # Swap bytes

def get_name_or_ip(hostip):
    # try to get hostname by ip

    try:
        host = socket.gethostbyaddr(hostip)
        nameorip = '{0} ({1})'.format(hostip, host[0])
    except Exception:
        nameorip = '{0} (host name could not be determined)'.format(hostip)
    return nameorip


def build_packet():
    # create header and append check sum, Header is type (8), code (8), checksum (16), id (16), seq (16)

    myChecksum = 0
    myID = os.getpid() & 0xFFFF  # Return the current process i. oxffff is used for control the length of pid

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)  # pack to  binary data
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    # if os is MAC OS
    if sys.platform == 'darwin':
        myChecksum = socket.htons(myChecksum) & 0xffff
        # Convert 16-bit integers from host to network byte order.
    else:
        # Convert 16-bit integers from host to network byte order.
        myChecksum = socket.htons(myChecksum)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    packet = header + data
    return packet


def get_route(hostname):
    print(label.format(hostname))
    # get the format  ********baidu.com*******


    for ttl in range(1, MAX_HOPS):  # ttl max = 30

        # try two times. send two packages
        for tries in range(TRIES):  #
            destAddr = socket.gethostbyname(hostname)
            timeLeft = TIMEOUT  # 2
            # Fill in start
            # Make a raw socket named mySocket
            icmp = socket.getprotobyname("icmp")
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)

            mySocket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))  #
            mySocket.settimeout(TIMEOUT)  # set  max reconnection time 2s

            try:
                d = build_packet()

                mySocket.sendto(d, (hostname, 0))
                t = time.time()

                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = time.time() - startedSelect

                if whatReady[0] == []:  # Timeout
                    print(" * * * Request timed out.")

                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()

                timeLeft = timeLeft - howLongInSelect
                if timeLeft <= 0:
                    print(" * * * Request timed out.")

            except socket.timeout:
                continue
            else:
                # Fill in start
                # Fetch the icmp type from the IP packet
                # why include [28]
                icmpHeaderContent = recvPacket[20:28]  # 0~19 is ip header
                type, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeaderContent)
                printname = get_name_or_ip(addr[0])


                # time exceeded
                if type == 11:
                    bytes = struct.calcsize("d")  # get the bytes number of "d"

                    # the payload has a timestamp  indicating the time of transmission
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print(" %d rtt=%.0f ms %s" % (ttl, (timeReceived - t) * 1000, printname))

                # destination unreachable
                elif type == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print(" %d rtt=%.0f ms %s" % (ttl, (timeReceived - t) * 1000, printname))

                # echo reply
                elif type == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print(" %d rtt=%.0f ms %s" % (ttl, (timeReceived - timeSent) * 1000, printname))
                    return
                else:
                    print("error")
                break
            finally:
                mySocket.close()


get_route("www.baidu.com")
