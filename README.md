
# Infrared Raspberry Pi Guide

Disclaimer this guide is from summer (about august) 2019. My gear is a Raspberry Pi 2 model B, 1GB, revision a01041 (Sony, UK).
As operating system I installed retropie and then LXDE, currently a Raspbian GNU/Linux 9 (stretch).


## Circuite

Short range version.


## Software

First big challange, most documentation I have found was using lirc-rpi kernel module. After
a lot of try and error I know that kernel module lirc-rpi is no longer supported. 
Currently versions of the raspberry pi kernel can interpret infrared input directly,
this gives the capability of mapping it to `/dev/input/eventX` as regular keyboard events. 
So any guide that start by adding `dtoverlay=lirc-rpi,...` is no longer useful, at least
the setup part, and should be ignored. If you are still skeptical refer to the links below.

[LibreELEC  infrared](https://wiki.libreelec.tv/infrared_remotes).

LibreELEC documentation is very throughful, eventhough this is not the exact same distribution it uses
the same kernel.

[Raspberry pi kernel(firmware) documentation](https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README)


So with that out of the way let us start by adding to the /boot/config.txt the needed information to
load the kernel modules at boot. I mapped the IR reader to GPIO18 and the IR LED to GPIO17, you
might change this if you use other pins on the Pi.

```
# this will enable to receive IR signals
dtoverlay=gpio-ir,gpio_pin=18,rc-map-name=ir-keytable
# this will enable to send IR signals
dtoverlay=gpio-ir-tx,gpio_pin=17
```

You can opitionally change the default GPIO pin connected, which is 18.
After editing this file we need to reboot.

```
sudo reboot
```

After the reboot process has finished you can open a terminal again and see if everything is
ok with the keytable command.

```
$ sudo ir-keytable 
Found /sys/class/rc/rc0/ (/dev/input/event4) with:
	Driver gpio_ir_recv, table rc-empty
	Supported protocols: other lirc rc-5 rc-5-sz jvc sony nec sanyo mce_kbd rc-6 sharp xmp 
	Enabled protocols: lirc mce_kbd 
	Name: gpio_ir_recv
	bus: 25, vendor/product: 0001:0001, version: 0x0100
	Repeat delay = 500 ms, repeat period = 125 ms

```

First thing it is important that this command run without errors. If the output is alike 
the above check the line that shows `Supported protocols` here you want to ensure your IR receiver 
supports lirc protocol. You can also check that `/dev/lircX` devices exist. You can check this with 
find command as below.

```
$ find /dev -name 'lirc*'
/dev/lircd
/dev/lirc1
/dev/lirc0
```

The correct output should list at least 2 lirc devices one for input and another for output. Apperently
nothing guarantees which is the input and output since this depend on the kernel however in my case it 
is pretty consistent that `/dev/lirc0` is output (IR LED) meanwhile `/dev/lirc1` is input (IR receiver).


Use `ir-ctl` program to check if it is working. You need to start the program with option record `-r`
then press any control remote button, poiting to the IR receiver of course. If everything is correct you
will see some text appears on the screen as you press buttons. An error like `/dev/lirc0: device cannot record raw ir`
means probably that the lirc0 points to the output device, try to use the option `-d` with `/dev/lirc1`.

```
$ ir-ctl -r -d=/dev/lirc1
pulse 9014
space 4518
pulse 570
...
```

This means you are finally making a button press from the IR remote go all the way 
to the IR receiver and inside the linux kernel code. Isn't it awesome!? You can record a button
from a simple controller using `ir-ctl -rFILENAME -d /dev/lirc1 -1 -P` you can check the options 
using `man ir-ctl` but basically `-rFILENAME` says to store the output on a file named FILENAME, `-1` stands for
one shot (that is it receives one set of input and then fnishes), `-P` is to avoid printing the timeout
on the end of the file which is just comestic so we don't get a warning message from the
ir-ctl send command. Now that you have working command try to send it using `ir-ctl --send FILENAME` where you
need to change FILENAME for with correct file.

```
ir-ctl --send FILENAME
```












