import  socket
def get_name_or_ip(hostip):

    try:
        host = socket.gethostbyaddr(hostip)
        nameorip = '{0} ({1})'.format(hostip , host[0])
    except Exception:
        nameorip = '{0} (host name could not be determined)'.format(hostip)
    print(nameorip)
get_name_or_ip("123.125.115.110")