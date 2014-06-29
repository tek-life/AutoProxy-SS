#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import socks
import socket
import urllib2
import datetime
import pdb
import subprocess

def _Config_proxy_():
  socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1084)
  socket.socket = socks.socksocket

def _Check_Speed_():
  os.system("sleep 2")
  _Config_proxy_()
  speed=[]
  for i in range(3):
    try:
      start = datetime.datetime.now()
      content = urllib2.urlopen('https://www.google.com',None,3).read()
    except urllib2.URLError:
      pass 
    except socks.ProxyConnectionError:
      pass
    else:
#    print len(content)
      end = datetime.datetime.now()
      delta = (end-start).seconds*1000.0+(end-start).microseconds
      _speed = len(content)*1000.0/delta
      if _speed < 100:
        print("%d -- %d" %(delta,_speed))
        speed.append(_speed)
  if speed==[]:
     return 0
  return sum(speed)/len(speed)

#print _Check_Speed_()

config = open("id.ini","r")
content = config.readlines()
content = [co[:-1:] for co in content]
#print content
#pdb.set_trace()
def _Read_One_Item(list_part, num):
  if num < 4:
    print("Error! The item is wrong\n")
    exit(-1);
  ip=list_part[0]#.encode("utf-8")
  ip=re.findall(r'：(\d*.{3,}\d+)',ip)
  port=list_part[1]#.encode("utf-8")
  port=re.findall(r'：(\d+)',port)
  password=list_part[2]
  password=re.findall(r'：(.+)',password)
  encry = list_part[3]
  encry = re.findall(r'：(.+)',encry)
  supporter = list_part[4]
  supporter = re.findall(r'：(.+)',supporter)
#  print [ip,port,password,encry,supporter]
  return_value = {"ip":"".join(ip),"port":"".join(port),"password":"".join(password),"encry":"".join(encry),"supporter":"".join(supporter)}
  return return_value

def Connect():
  pass

def _Check_Content():
  for fo in content:
    print(fo)

def foo():
#  _Check_Content()
  length = len(content)
  iter_i = 0
  temp = []
  temp = content
  max_speed=0
  temp_speed=0.0
  max_config=[]
  nex=0
 
  while iter_i < length:
    str_li=[]
    _config_li= _Read_One_Item(temp,5)
    str_li.append("sslocal")
#    str_li.append(_config_li["ip"])
    str_li.append("-s")
    str_li.append(_config_li["ip"])
    str_li.append("-p")
    str_li.append(_config_li["port"])
    str_li.append("-k")
    str_li.append(_config_li["password"])
    str_li.append("-m")
    str_li.append(_config_li["encry"])
    str_li.append("-l")
    str_li.append("1084")
#    print str_li
    child=subprocess.Popen(str_li)
#    if nex == 0:
    temp_speed = _Check_Speed_()
    print("IP:%s 's speed %d \n"%(_config_li["ip"],temp_speed))
    child.kill()
    if temp_speed > max_speed:
       max_config=str_li[:]
       max_speed=temp_speed
#       max_str_config=str_li
#    print iter_i
    iter_i+=5
    temp=temp[5: ]
    nex += 1
  
  print("WIN: %s -- %d\n"%("".join(max_config),max_speed))
  child=subprocess.Popen(max_config)

if __name__ == '__main__':
  foo()
