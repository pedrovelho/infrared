#!/usr/bin/python3

import sys

##
# Check if the value a is in the range of b with degree of
# tolerance +/- 20 %. This means if a is in the interval 
# [b - 20% , b + 20%] return true, otherwise return false.
##
def inRange(a,b):
    tolerance=b*0.18
    if (b-tolerance) < a < (b+tolerance):
        return True
    return False

byteCounter=0
bitCounter=0
byteSequence=''

for line in sys.stdin:
    info = line.rstrip().split(' ')

    # decode the string
    if info[0] == 'pulse' and inRange(int(info[1]),30000):
        print('PULSE 30000')
    elif info[0] == 'pulse' and inRange(int(info[1]),3400):
        print('PULSE 3400')
    elif info[0] == 'pulse' and int(info[1]) < 2000:
        print('', end='')
        # ignore this is just a bit separator
    elif info[0] == 'space' and inRange(int(info[1]), 50000):
        print('\nSPACE 50000')
    elif info[0] == 'space' and inRange(int(info[1]), 42000):
        print('\nSPACE 42000')
        # This comes just after space 1700 and means a sequence starts
    elif info[0] == 'space' and inRange(int(info[1]),1700):
        print('SPACE 1700')
    # Long pause = 1
    elif info[0] == 'space' and inRange(int(info[1]),1200):
        byteSequence = '1' + byteSequence
        bitCounter += 1
    # Short pause = 0
    elif info[0] == 'space' and int(info[1]) < 1000:
        byteSequence = '0' + byteSequence
        bitCounter += 1
    elif info[0] == 'timeout':
        print('\nEND OF INPUT - timeout')
        print('bitCounter ', bitCounter)
        print('byteCounter ', byteCounter)
        byteCounter=0
    else:
        print('Unrecognized sequence : ', info)

    if bitCounter == 8:
        print(byteSequence, end=' ')
        bitCounter = 0
        byteSequence = ''
        byteCounter += 1
        if (byteCounter % 4) == 0:
            print('')
	
