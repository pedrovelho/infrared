#!/usr/bin/python3

import sys

def binaryXor(b1,b2):
    if len(b1) != len(b2):
        print('Error operators must be of same size')
    r = ''
    for i in range(len(b1)-1, -1, -1):
        if b1[i] == '1' and b2[i] == '1':
            r = '0' + r
        elif b1[i] == '0' and b2[i] == '0':
            r = '0' + r
        else:
            r = '1' + r
    return r


for line in sys.stdin:
    byteArray = line.rstrip().split(' ')
    sum = '00000000'
    for i in byteArray:
        sum = binaryXor(sum, i)


checkbit = sum[0]
for i in range(1, len(sum), 1):
    if checkbit != sum[i]:
        checkbit = '1'
    else:
        checkbit = '0'

checksum = sum[0: len(sum)-1]
checksum += checkbit

print('checkbit is = '+checkbit)
print('checksum is = '+checksum)