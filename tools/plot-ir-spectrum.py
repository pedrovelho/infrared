#!/usr/bin/python3

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


#echo "set xlabel 'time'" >> temp.gnuplot
#echo "set ylabel 'state'" >> temp.gnuplot
#echo "plot './temp.dat' using 2:1 with lp" >> temp.gnuplot
#gnuplot temp.gnuplot --persist