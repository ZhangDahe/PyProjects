def checksum(str):
# In this function we make the checksum of our packet
    csum = 0
    countTo = (len(str) / 2) * 2
    count = 0
    while count < countTo:
        #ord  Return the Unicode code point for a one-character string
        thisVal = ord(str[count+1]) * 256 + ord(str[count])
        print(thisVal)
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
    if countTo < len(str):
        csum = csum + ord(str[len(str) - 1])
        csum = csum & 0xffffffff
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer
print(checksum('12345'))