
# Hitachi rar-6n1

This is the reverse engeneering of my rar-6n1 Hitachi remote control. Air-conditioning
has 2 indoor units and a single outdoor unit.



## Signal shape

Every sequence starts by a pulse of 30000us. The sequence might containe 1 or 2 chuncks
of bits, each chunk sequence start by:

```
SPACE 50000
PULSE 3400
SPACE 1700
```


Following data is decoded using short pulses of around 420us in the service manual.
My tests indicate that best is recognize any pulse shorter than 1000us as separators. 
After each separator pulse we can have either a 1200us space (binary '1') or a short space 
less than 1000us (binary '0'). See below an example with real raw data.


```
pulse 29945 => START PULSE
space 49867 -.
pulse 3405  -'==> CHUNK START
space 1640  -'
pulse 472   => BIT SEPARATOR PULSE
space 1219  => BINARY 1
pulse 471   => BIT SEPARATOR PULSE
space 453   => BINARY 0
...
```


As you can see the timing is approximative, my decoding python program has a tolerance
of 18% of the nominal value when comparing. For short pulses or spaces it uses a regular
less then comparison.



```python
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

```


We can identify 3 types os sequences, first a 

### Long sequence (44 bytes in 2 chunks, 28 bytes first chunk + 16 bytes second chunk)

This sequence is trigered when pressing either the mode button or power button.

```
PULSE 30000

SPACE 50000
PULSE 3400
SPACE 1700
28 bytes LSB first

SPACE 50000
PULSE 3400
SPACE 1700
16 bytes LSB first
```

Total of 352 bits or 44 bytes.

### Short sequence (21 bytes in a single chunk)

Just works with the info button that displays the current room temperature on the remote.

```
PULSE 30000

SPACE 50000
PULSE 3400
SPACE 1700
21 bytes LSB first
```

Total of 168 bits or 21 bytes.

### Regular sequence (28 bytes in a single chunk)

Mostly any other button that is neither power, mode, or info.

```
PULSE 30000

SPACE 50000
PULSE 3400
SPACE 1700
28 bytes LSB first
```

Total of 224 bits or 28 bytes.










