# VibeLight Gateway

The [VibeLight Gateway](https://sicherheitskritisch.de/2016/03/cooles-rgb-led-stimmungslicht-diy-steuerbar-mit-smartphone-app/) transforms your Raspberry Pi to a cool ambiance light gateway. It allows to control WS2812B RGB-LEDs with your smartphone, tablet computer or normal desktop. By default the system provides some cool effects like: 

- Ambiance light (choose between 16 million colors)
- Rainbow effect
- Party mode with adjustable speed (beats per minute)

The system has a quite simple architecture (only HTML and Python), you can extend it easy with own effects if you want.

The effects can be easily controlled with your smartphone:

![VibeLight Gateway web app](https://sicherheitskritisch.de/images/vibelight-gateway-webapp-small.png)

The party mode with adjustable speed:

![VibeLight Gateway party mode](https://sicherheitskritisch.de/images/vibelight-gateway-party-mode-small.gif)

## Package building

**Note:** This should work properly on Raspbian / Debian 8 (Jessie).

First install the packages for building:

    ~$ sudo apt-get update
    ~$ sudo apt-get install devscripts dh-systemd

Than clone this repository:

    ~$ git clone https://github.com/bastianraschke/vibelightgateway.git

Build the package:

    ~$ cd ./vibelightgateway/src/
    ~$ debuild

## Installation

First install the NeoPixel library from Adafruit according to the [documentation](https://learn.adafruit.com/neopixels-on-raspberry-pi/software):

    ~$ sudo apt-get install build-essential python-dev git scons swig

    ~$ git clone https://github.com/jgarff/rpi_ws281x.git
    ~$ cd ./rpi_ws281x/
    ~$ scons

    ~$ cd ./python/
    ~$ sudo python setup.py install

Than install the built VibeLight Gateway Debian package:

    ~$ sudo dpkg -i ../vibelight-gateway*.deb

Install missing dependencies:

    ~$ sudo apt-get -f install

## Deployment

The last step is the deployment of the web app (HTML files) via a normal webserver. Furthermore the VibeLight Gateway websocket server should be proxied with the webserver aswell.

Install Nginx and delete default configuration:

    ~$ sudo apt-get install nginx
    ~$ sudo rm /etc/nginx/sites-enabled/default

Copy and activate the provided example configuration:

    ~$ cd /usr/share/doc/vibelight-gateway/examples/configuration/nginx/

    ~$ sudo cp ./nginx.conf /etc/nginx/nginx.conf
    ~$ sudo cp ./sites-enabled/vibelightgateway.conf /etc/nginx/sites-enabled/vibelightgateway.conf
    ~$ sudo ln -s /etc/nginx/sites-available/vibelightgateway.conf /etc/nginx/sites-enabled/vibelightgateway.conf

Provide the correct directory for Nginx and restart:

    ~$ sudo rm /usr/share/nginx/www
    ~$ sudo ln -s /usr/share/vibelight-gateway/webapp/ /usr/share/nginx/www

    ~$ sudo systemctl restart nginx.service

From now on the web app should be accessable on the machines network address.

## Questions

If you have any questions to this project, just ask me via email:

<bastian.raschke@posteo.de>
