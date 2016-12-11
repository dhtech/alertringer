#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""this is the receiver for alertringer"""

from bottle import route, run, template, get, put, post, request, error, abort, response, auth_basic
import json
import requests
import logging
import redis
import time

debug = True

@get('/api/v1/alerts')
def get_alerts():
  """
  list all alerts by key redis
  """
  remote_ip = request.environ.get('REMOTE_ADDR')
  data = []
  for key in r.scan_iter():
    data.append(key)
  logger.info('sent len: %i get_alerts to %s' % (len(data), remote_ip))
  response.content_type = 'application/json'
  return json.dumps(data, indent=4)


@post('/api/v1/alerts')
def post_alerts():
  """
  get the alerts from alertmanager and put it in the redis
  """
  try:
    remote_ip = request.environ.get('REMOTE_ADDR')
    redis_data = {}
    json_data = request.json
    redis_id = json_data['groupKey']
    redis_data['team'] = request.query['team']
    redis_data['status'] = json_data['status']
  except:
    if debug:
      logger.info('debug except: %s' % (str(sys.exc_info())))
    response.status = 400
    response.content_type = 'application/json'
    logger.info('failed post alert resv %s' % (remote_ip))
    return {'result': 'failed', 'message': 'json blob was not readable'}

  if redis_data['team'] not in teams:
    logger.info('team: %s not in teams: %s' % (redis_data['team'], str(teams)))
    response.status = 400
    response.content_type = 'application/json'
    return {'result': 'failed', 'message': 'team not valid'}

  if redis_data['status'] == "firing":
    logger.info('firing: key %s, team: %s from %s' % (redis_id, redis_data['team'], remote_ip)) 
    r.setex(str(redis_id)+':'+redis_data['team'], 600, json.dumps(redis_data))
  else:
    logger.info('resolved: key %s, team: %s from %s' % (redis_id, redis_data['team'], remote_ip))
    try:
      r.delete(str(redis_id)+':'+redis_data['team'])
      if debug:
        logger.info('deleted from db')
    except:
      if debug:
        logger.info('except: %s' % (sys.exc_info()))


if __name__ == '__main__':
  logger = logging.getLogger("reciver")
  logfile = '/var/log/alertringer.log'
  logger.setLevel(logging.INFO)
  formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  handler = logging.FileHandler(logfile)
  handler.setFormatter(formatter)
  logger.addHandler(handler)

  logger.info('starting up')
  teams = ['services','core','access','powerpatrol']
  r = redis.StrictRedis(host='localhost', port=6379, db=0)
  run(host='0.0.0.0', port=80, debug=False, reloader=False)
