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
more info regarding lib https://github.com/jgarff/rpi_ws281x
disable sound on the pi

```

* install
```

apt-get install git redis-server python3-pip python3-redis python3-requests python3-bottle python3-rpi.gpio
pip3 install rpi_ws281x

cd /opt
git clone https://github.com/dhtech/alertringer.git
cd alertringer
cp *.service /lib/systemd/system/
systemctl enable alertringer.service
systemctl enable alertbuzzer.service
systemctl enable alertreceiver.service
```

