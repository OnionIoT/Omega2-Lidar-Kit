#!/bin/sh

wget https://www.virtualhere.com/sites/default/files/usbserver/vhusbdmipsel -O /usr/bin/vhusbdmipsel
chmod +x /usr/bin/vhusbdmipsel
wget https://raw.githubusercontent.com/OnionIoT/omega2-lidar-kit/master/scripts/virtualhere -O /etc/init.d/virtualhere
chmod +x /etc/init.d/virtualhere
/etc/init.d/virtualhere enable
/etc/init.d/virtualhere start
