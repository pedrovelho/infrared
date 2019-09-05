
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

This sequence is trigered when pressing either the mode, power, or sleep buttons.
The second chunk is the time and date so that the remote and indoor unit synchronize during
time related operations.

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

## Bytes meaning of regular and long sequences

### First CHUNK

* Byte 1-7      : fixed  x01 x10 x30 x40 xBF x01 xFE

* Byte 8        : 
    * 00010010 (18) when it is a long sequence, 2 chunks and 44 bytes
    * 00010001 (17) otherwise

* Byte 9        : fixed x12 (18)

* Byte 10       : changed with button pressed
    * power     : 0000 0011 3
    * mode      : 0000 0111 7
    * temp_up   : 0000 1000 8
    * temp_down : 0000 1001 9
    * fan       : 0000 1100 12
    * vswing    : 0000 1101 13
    * hswing    : 0000 1100 14
    * sleep     : 0001 0001 17
    * leavehome : 0001 0010 18
    * powerful  : 0001 0101 21
    * eco       : 0001 1000 24
    * silent    : 0001 1100 28
    * clean     : 0010 0001 33

* Byte 11       : Mode selection
    * sample 2 : 00000011  (3) => heat
    * sample 3 : 00000101  (5) => dry
    * sample 4 : 00000100  (4) => cool
    * sample 5 : 00001100 (12) => fan
    * sample 6 : 00000010  (2) => auto

* Byte 12    : temperature value * 2 (?left shifted), for instance:
    * sample 1  : 00100000 => 32 / 2 = 16 Celsius
    * sample 11 : 00101010 => 42 / 2 = 21 Celsius
    * sample 12 : 00101100 => 44 / 2 = 22 Celsius 
    * sample 13 : 00101110 => 46 / 2 = 23 Celsius

* Byte 13    : fixed x00

* Byte 14    : fan speed
    * 1 : 1 bar on the remote
    * 2 : 2 bars on the remote
    * 3 : 3 bars on the remote
    * 4 : 4 bars on the remote
    * 5 : auto fan on the remote

* Byte 15    : 00001010 (6) => stop vswing, 0001011 (7) activate vswing 

* Byte 16    : 00001010 (6) => stop hswing, 0001011 (7) activate hswing

* Byte 17    : fixed x00

* Byte 18    : 10000000 (128) => if power on, 0 otherwise

* Byte 19-20 : minutes before turn-off when on sleep mode, 
            read (byte20 byte19) as a single 2 byte number
            where byte 19 is the less significant
  * sample 42 : 0000 0000 0011 1100 (60)  x003C : 1 hour 
  * sample 43 : 0000 0000 1001 1000 (120) x0078 : 2 hours
  * sample 44 : 0000 0000 1011 0100 (180) x00B4 : 3 hours
  * sample 45 : 0000 0001 1010 0100 (420) x01A4 : 7 hours
  * sample 47 : 0000 0001 0000 0000 (256) x0100 : 256 minutes for leavehome
  * sample 46 : 0000 0000 0000 0000 (0)   x0000 : off


* Bytes 21-25 : fixed x00 x00 x00 x80 x01 (might be the time calendar)

* Byte 26    : where: 
    * samples 21-31 : 00000010 (2)  => eco mode on
    * sample  32    : 00100000 (32) => powerful on
    * 0 otherwise

* Byte 27    : 0001000 (8)  => silent on, 0 otherwise

* Byte 28    : modular sum of 2 complement's of 1-27 bytes added with 
    2 complement's of 01000010 (62)

### Second CHUNK

I believe this is for sync date and time. So after each mode, sleep or power command 
the indoor unit syncs with the remote.

* Bytes 29 - 35 : fixed x01 x10 x30 x40 xBF 0x10 0xEF
* Bytes 36 - 37 : fixed x22 x06
* Byte 38 : year, in 2 decimal digits (19 for 2019) x13
* Byte 39 : month, examples: 08 is august, 09 is september
* Byte 40 : day of month
* Byte 41 : hour
* Byte 42 : minutes
* Byte 43 : day of week [1-7] meaning [monday - sunday]
* Byte 44 : modular sum of 2 complement's of bytes 29-43 added with 
    2 complement's of 01000010 (62)


