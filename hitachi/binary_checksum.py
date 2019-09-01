#!/usr/bin/python3

import sys

def binaryAdd(b1,b2):
    if len(b1) != len(b2):
        print('Error operators must be of same size')
    carryBit = '0'
    r = ''
    for i in range(len(b1)-1, -1, -1):
        if b1[i] == '1' and b2[i] == '1':
            if carryBit == '1':
                r = '1' + r
            else:
                r = '0' + r
            carryBit = '1'
        elif b1[i] == '0' and b2[i] == '0':
            if carryBit == '1':
                r = '1' + r
            else:
                r = '0' + r
            carryBit = '0'
        else:
            if carryBit == '1':
                r = '0' + r
            else:
                r = '1' + r
        #print(b1[i]+' '+b2[i]+' '+carryBit+' '+r[0])
    return r


def byte2int(b1):
    val = int(b1, 2)
    if val > 127:
        return str(val-256)
    else:
        return str(val)


def test():
    a='10011001'
    b='00110010'
    print(a+' = '+byte2int(a))
    print(b+' = '+byte2int(b))
    print('Result is')
    result = binaryAdd(a,b)
    print(result+' = '+byte2int(result))


for line in sys.stdin:
    byteArray = line.rstrip().split(' ')
    sum = '00000000'

    for i in byteArray:
        sum = binaryAdd(sum, i)

    print('Row checkSum is '+sum)