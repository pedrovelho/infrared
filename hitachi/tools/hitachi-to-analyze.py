#!/usr/bin/python3

import sys

##
# Check if the value a is in the range of b with degree of
# tolerance +/- 18 %. This means if a is in the interval 
# [b - 18% , b + 18%] return true, otherwise return false.
##
def inRange(a,b):
    tolerance=b*0.18
    if (b-tolerance) < a < (b+tolerance):
        return True
    return False

byteCounter=0
bitCounter=0
byteSequence=''
transmissionTime=0
hexSequence=''
for line in sys.stdin:
    info = line.rstrip().split(' ')

    if info[0] == 'pulse' or info[0] == 'space':
        transmissionTime+=int(info[1])
    # decode the string
    if info[0] == 'pulse' and inRange(int(info[1]),30000):
        print('\nPULSE 30000')
    elif info[0] == 'pulse' and inRange(int(info[1]),3400):
        print('PULSE 3400')
    elif info[0] == 'pulse' and int(info[1]) < 2000:
        print('', end='')
        # ignore this is just a bit separator
    elif info[0] == 'space' and inRange(int(info[1]), 50000):
        print('\nSPACE 50000')
    elif info[0] == 'space' and inRange(int(info[1]), 42000):
        print('\nSPACE 42000')
    elif info[0] == 'space' and inRange(int(info[1]),1700):
        print('SPACE 1700')
    # Long pause = 1
    elif info[0] == 'space' and inRange(int(info[1]),1200):
        byteSequence = '1' + byteSequence
        bitCounter += 1
        print('1', end='')
    # Short pause = 0
    elif info[0] == 'space' and int(info[1]) < 1000:
        byteSequence = '0' + byteSequence
        bitCounter += 1
        print('0', end='')
    elif info[0] == 'timeout':
        print('\nEND OF INPUT - timeout')
        print('bitCounter ', bitCounter)
        print('byteCounter ', bitCounter/8)
        print('transmission time (kernel default max 500ms): ', transmissionTime)
        bitCounter=0
        byteSequence=''
        print('HEX SEQUENCE '+hexSequence)
        hexSequence=''
        transmissionTime=0
    else:
        print('Unrecognized sequence : ', info)

	
