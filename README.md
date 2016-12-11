# alertringer
An audio-visual experience for rendering prometheus alerts

* prereqs
```
* 1 raspberry 3
* 4 neopixelrings 24 leds
* passive buzzer
* 5V 5A powersupply

a passive buzzer is connected to GPIOpin21 and ground
the leds are linked in serial and the first one is directly connected to gpiopin 18 on the rpi3 
https://www.adafruit.com/products/1586
sound borrowed from https://github.com/gumslone/raspi_buzzer_player
```

* install
```
compile and install, dont forget to disable the builtin sound
https://github.com/jgarff/rpi_ws281x

apt-get install redis-server
cd /opt
git clone https://github.com/dhtech/alertringer.git
cd alertringer
cp *.service /lib/systemd/system/
systemctl enable alertringer.service
systemctl enable alertbuzzer.service
systemctl enable alertreceiver.service
```

