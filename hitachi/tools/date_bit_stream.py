#!/usr/bin/python3
from datetime import datetime, date

def getByteStream(time):
    byteStream = [0x01, 0x10, 0x30, 0x40, 0xbf, 0x10, 0xef, 0x22, 0x06, # Fixed
                0x38, 0x39, 0x40, 0x41, 0x42, 0x43, 0x44 ] # date
    byteStream[9] = time.year - 2000
    byteStream[10] = time.month
    byteStream[11] = time.day
    byteStream[12] = time.hour
    byteStream[13] = time.minute
    byteStream[14] = time.weekday()+1
    byteStream[15] = parity(byteStream)
    return byteStream

def twoComplement(x):
    if x == 128 :
        return x
    elif x >= 0 and x < 128 :
        return -1*x
    elif x >= 128 and x < 256 :
        return -1*(x - 256)
    else :
        print("fail x out of range")
        return(0)

def parity(byteStream):
    sum = 0
    for i in range(0, len(byteStream)-1, 1):
        sum += twoComplement(byteStream[i])
    sum += 62
    if sum < 0:
        return 256 + sum
    else:
        return sum

# less significant bit first, so 1 is 10000000, 81 is 10001010
def dec2binLSB(x):
    bitString = ''
    for i in range(0, 8, 1):
        bitString += str(x%2)
        x = x//2
    return bitString

def genBitStream(curDate):
    st = getByteStream(curDate)
    answer = ''
    for i in range(0, len(st), 1):
        answer += dec2binLSB(st[i])
    return answer


t1 = datetime(year = 2019, month = 8, day = 28, hour = 20, minute = 57)
result = genBitStream(t1)
expected = '10000000000010000000110000000010111111010000100011110111010001000110000011001000000100000011100000101000100111001100000000001010'
print('RESULT   ', result)
print('EXPECTED ',expected)
if result == expected :
    print('SUCCESS! strings match!')

print('STRING FOR NOW IS ', genBitStream(datetime.now()))
