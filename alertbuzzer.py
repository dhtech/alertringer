#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import redis
import sys
import signal
import logging
import buzzer

logfile = '/var/log/alertringer.log'
debug = True

logger = logging.getLogger("buzzer")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler(logfile)
handler.setFormatter(formatter)
logger.addHandler(handler)


def signal_handler(signal, frame):
  logger.info('shutting down')
  buzzer.destroy()
  exit()


if __name__ == '__main__':
  buzzer.setup()
  firstrun = True
  logger.info('starting up')
  signal.signal(signal.SIGTERM, signal_handler)
  r = redis.StrictRedis(host='localhost', port=6379, db=0)
  teams = {'access': 0, 'core': 0, 'powerpatrol': 0, 'services': 0} 
  while True:
    time.sleep(1)
    oldteams = teams.copy()
    teams = {'access': 0, 'core': 0, 'powerpatrol': 0, 'services': 0}
    for key in r.scan_iter():
      val = r.get(key)
      if val is None:
        if debug:
          print(key)
      else:
        team = json.loads(val.decode('utf-8'))['team']
        teams[team] = teams[team] +1
    if firstrun == True:
      firstrun = False
      continue
    if teams != oldteams:
      if teams['services'] > oldteams['services']:
        logger.info('playing services')
        firstrun = True
        buzzer.play(buzzer.popcorn_melody, buzzer.popcorn_tempo, 0.50, 1.000)
        continue
      if teams['core'] > oldteams['core']:
        logger.info('playing core')
        firstrun = True
        buzzer.play(buzzer.star_wars_melody, buzzer.star_wars_tempo, 0.50, 1.000)
        continue
      if teams['access'] > oldteams['access']:
        logger.info('playing access')
        firstrun = True
        buzzer.play(buzzer.crazy_frog_melody, buzzer.crazy_frog_tempo, 0.30, 0.900)
        continue
      if teams['powerpatrol'] > oldteams['powerpatrol']:
        logger.info('playing powerpatrol')
        firstrun = True
        buzzer.play(buzzer.final_countdown_melody, buzzer.final_countdown_tempo, 0.30, 1.2000)
        continue

