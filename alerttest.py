#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""util script for testing send stuff 2 redis via alertreceiver"""

import json
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--key', type=int, default=123, help='groupkey for faking alarms')
parser.add_argument('--status', type=str, default='firing', choices=['firing','resolved'], help='alert or unalert')
parser.add_argument('--team', type=str, default='core', choices=['services','core','access','wifi','powerpatrol'], help='team for blaming')
parser.add_argument('--keys', action='store_true', help='get all keys from redis')

args = parser.parse_args()


url = 'http://127.0.0.1:80/api/v1/alerts'
headers = {"content-type": "application/json; charset=utf-8"}

if args.keys:
  r = requests.get(url, headers=headers)
  print(r.json())
  exit()

data = {}
data['groupKey'] = args.key
data['status'] = args.status
paramdata = {}
paramdata['team'] = args.team

r = requests.post(url, headers=headers, json=data, params=paramdata)
print(data, paramdata, r.text)
print(r.status_code)


