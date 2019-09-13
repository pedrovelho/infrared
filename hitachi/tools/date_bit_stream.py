#!/usr/bin/python3
from datetime import datetime, date

# Get the byte array that carries a datetime sync with hitachi AC
def getDateByteStream(time):
    byteStream = [
                0x01, 0x10, 0x30, 0x40, 0xbf, 0x10, 0xef, # Fixed
                0x22, 0x06, # Fixed
                0x38, 0x39, 0x40, 0x41, 0x42, 0x43, # date and time
                0x44 # parity byte
    ]
    byteStream[9] = time.year - 2000
    byteStream[10] = time.month
    byteStream[11] = time.day
    byteStream[12] = time.hour
    byteStream[13] = time.minute
    byteStream[14] = time.weekday()+1
    byteStream[15] = parity(byteStream)
    return byteStream

# Get a numeric representation in decimal of the 2 complement's of a given x
def twoComplement(x):
    if 0 <= x < 128 :
        return -1*x
    elif x == 128 : # 2 complement's of 128 is itself
        return x
    elif 128 < x < 256 :
        return -1*(x - 256)
    else :
        print("Failed because x was out of range!!!")
        return(0)

# The parity function, sum of 2 complement's of n-1 bytes, and then add 62
# Decode the bitString in a single unsigned int in interval [0,255]
def parity(byteStream):
    sum = 0
    for i in range(0, len(byteStream)-1, 1):
        sum += twoComplement(byteStream[i])
    sum += 62 # 0011 1110
    if sum < 0:
        return 256 + sum
    else:
        return sum

# Convert unsigned int in [0,255] in a bit string with
# less significant bit first, i.e. 1 is 10000000, 81 is 10001010
def dec2binLSB(x):
    bitString = ''
    for i in range(0, 8, 1):
        bitString += str(x%2)
        x = x//2
    return bitString

# Based on a date get the bit string that represents it with parity bit and
# fixed bytes.
def genDateBitStream(curDate):
    st = getDateByteStream(curDate)
    answer = ''
    for i in range(0, len(st), 1):
        answer += dec2binLSB(st[i])
    return answer


timeTable = [
datetime(year = 2019, month = 8, day = 28, hour = 20, minute = 57),
datetime(year = 2019, month = 9, day =  3, hour =  5, minute = 34),
datetime(year = 2019, month = 8, day = 28, hour = 21, minute = 2 ),
datetime(year = 2019, month = 8, day = 28, hour = 21, minute = 6 ),
datetime(year = 2019, month = 8, day = 28, hour = 21, minute = 7 ),
datetime(year = 2019, month = 8, day = 28, hour = 21, minute = 13),
datetime(year = 2019, month = 8, day = 28, hour = 21, minute = 16),
datetime(year = 2019, month = 8, day = 29, hour =  5, minute =  4),
datetime(year = 2019, month = 9, day =  3, hour =  5, minute = 31),
datetime(year = 2019, month = 9, day =  3, hour =  5, minute = 26),
datetime(year = 2019, month = 9, day =  3, hour =  5, minute = 28),
datetime(year = 2019, month = 9, day =  3, hour =  5, minute = 38),
datetime(year = 2019, month = 9, day =  3, hour =  5, minute = 38),
datetime(year = 2019, month = 9, day =  3, hour =  5, minute = 39),
datetime(year = 2019, month = 9, day =  3, hour =  5, minute = 41),
datetime(year = 2019, month = 9, day =  3, hour =  5, minute = 42),
datetime(year = 2019, month = 9, day =  3, hour =  5, minute = 44),
datetime(year = 2019, month = 9, day =  3, hour =  5, minute = 45),
datetime(year = 2019, month = 9, day =  3, hour =  5, minute = 47)
]

expected = [
"10000000000010000000110000000010111111010000100011110111010001000110000011001000000100000011100000101000100111001100000000001010",
"10000000000010000000110000000010111111010000100011110111010001000110000011001000100100001100000010100000010001000100000011110001",
"10000000000010000000110000000010111111010000100011110111010001000110000011001000000100000011100010101000010000001100000001100001",
"10000000000010000000110000000010111111010000100011110111010001000110000011001000000100000011100010101000011000001100000001000001",
"10000000000010000000110000000010111111010000100011110111010001000110000011001000000100000011100010101000111000001100000010000001",
"10000000000010000000110000000010111111010000100011110111010001000110000011001000000100000011100010101000101100001100000011011110",
"10000000000010000000110000000010111111010000100011110111010001000110000011001000000100000011100010101000000010001100000000011110",
"10000000000010000000110000000010111111010000100011110111010001000110000011001000000100001011100010100000001000000010000001001001",
"10000000000010000000110000000010111111010000100011110111010001000110000011001000100100001100000010100000111110000100000001001001",
"10000000000010000000110000000010111111010000100011110111010001000110000011001000100100001100000010100000010110000100000011101001",
"10000000000010000000110000000010111111010000100011110111010001000110000011001000100100001100000010100000001110000100000010101001",
"10000000000010000000110000000010111111010000100011110111010001000110000011001000100100001100000010100000011001000100000011010001",
"10000000000010000000110000000010111111010000100011110111010001000110000011001000100100001100000010100000011001000100000011010001",
"10000000000010000000110000000010111111010000100011110111010001000110000011001000100100001100000010100000111001000100000001010001",
"10000000000010000000110000000010111111010000100011110111010001000110000011001000100100001100000010100000100101000100000000010001",
"10000000000010000000110000000010111111010000100011110111010001000110000011001000100100001100000010100000010101000100000011100001",
"10000000000010000000110000000010111111010000100011110111010001000110000011001000100100001100000010100000001101000100000010100001",
"10000000000010000000110000000010111111010000100011110111010001000110000011001000100100001100000010100000101101000100000000100001",
"10000000000010000000110000000010111111010000100011110111010001000110000011001000100100001100000010100000111101000100000001000001"
]

for i in range(0, len(timeTable)):
    print("===================================")
    print("Running test case # ", i)
    result = genDateBitStream(timeTable[i])
    if result == expected[i] :
        print('SUCCESS! strings match!')
    else :
        print('FAILED! test failed!')
        print('RESULT   ', result)
        print('EXPECTED ',expected)


print('STRING FOR NOW IS ', genDateBitStream(datetime.now()))
