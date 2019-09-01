#!/usr/bin/python3

import sys

byteArray = []
# Create an array with all bytes
for line in sys.stdin:
    byteArray += line.rstrip().split(' ')


def tohex(val, nbits):
    return hex((val + (1 << nbits)) % (1 << nbits))

def tobin(val, nbits):
    return bin((val + (1 << nbits)) % (1 << nbits))

def get_parity_block(inp_val):
    #running_total=int(inp_val[0],2)
    running_total=0
    for i in range(0,len(inp_val)):
        running_total^=int(inp_val[i],2)
    return running_total


# try all possible sizes
#for i in range(0, len(byteArray)):
#    for j in range(i+1, len(byteÄrray)):


#def createSet(size, )

res=get_parity_block(byteArray[8:len(byteArray)-1])

print ("Byte 12 (hex):\t",tohex(int(byteArray[11],2),8), "  value="+byteArray[11])
print ("Block parity (hex):\t",tohex(res,8))
print ("Block parity (bin):\t", "{:b}".format(res%256))
print ("Expected (hex):\t",tohex(int(byteArray[len(byteArray)-1],2),8))
print ("Expected (bin):\t",byteArray[len(byteArray)-1])
