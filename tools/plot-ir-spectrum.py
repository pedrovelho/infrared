#!/usr/bin/python3

# Usage, $ cat rawdatafile | ./plot-ir-spectrum.py

import sys

timeStamp=0

for line in sys.stdin:
    info = line.rstrip().split(' ')

    # decode the string
    if info[0] == 'pulse':
        print(timeStamp+1, ' 1')
        timeStamp += int(info[1])
        print(timeStamp, ' 1')
    elif info[0] == 'space':
        print(timeStamp+1, ' 0')
        timeStamp += int(info[1])
        print(timeStamp, ' 0')



#set yrange [0:50000]
#set xrange [-0.1:1.1]
#plot '/tmp/tmp.dat' w lp 2


#system('gnuplot /tmp.gp')
