
# Omega2 Wireless LiDAR Kit

See the [Omega2 Wireless LiDAR Kit Quickstart](https://onion.io/omega2-wireless-lidar-kit-quickstart) for full details.

Repo contents:

* [scripts](./scripts) - Scripts to install VirtualHere Remote USB Server on your Omega
* [bin](./bin) - LiDAR scanner visualization software
* [specs](./specs) - LiDAR specifications
* [src](./src) - Example code

## Installation Instructions

The VirtualHere software facilitates wireless transmission of LiDAR data to Computer.

### Install the VirtualHere Remote USB Server on your Omega

Run the following on the Omega command line:

```
wget -O - https://raw.githubusercontent.com/OnionIoT/omega2-lidar-kit/master/scripts/autoSetup.sh | sh
```

### For instructions to install computer side client

Visit VirtualHere official Website: [VirtualHere USB Client](https://www.virtualhere.com/usb_client_software)

## Example Code

See [src](./src) directory for example Python3 code that interprets serial data coming from the LiDAR scanner. Can be run on a Computer or the Omega.

