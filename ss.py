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
import Image
import zbar
import qrcode
import ssl
import base64

special_char=[':','@',':']
special_corresp=['encry','password','ip','port']
str_li=[]
local_port=1080
Speed_check_number=3
sslocal_flag=False


#qrPath is the QR image's URL
#Will return the qrpath from qr
def _Decodeqr(qrPath):
    print(qrPath)
    try:
      content = urllib2.urlopen(qrPath,None,3).read()
    except (ssl.SSLError,urllib2.URLError, socks.ProxyConnectionError):
      print("Read %s timeout"%qrPath)
      return {}
    qrfile = "/tmp/qr.png"
    qrf = open(qrfile,"wr")
    qrf.write(content)
    qrf.close()
#    print content
    scanner = zbar.ImageScanner()
    scanner.parse_config('enable')
    pil = Image.open(qrfile).convert('L')
    width, height = pil.size
 
    raw = pil.tostring()
 
    image = zbar.Image(width,height,'Y800', raw)
 
    scanner.scan(image)
 
    data = {}
 
    for symbol in image:
        #print type(symbol.type) #<type 'zbar.EnumItem'>
        data[str(symbol.type)] = symbol.data
 
    del(image)
    return data


#Get the page of free id webpage

def _Get_QR_Png():   
  url_path="https://www.shadowsocks.net/get"
  print("Reading page from %s"%url_path)
  try:
    page=urllib2.urlopen(url_path,None,5).read()
  except Exception:
    print("""Could get the page of shadowsocks.net/get\n 
  	 Please Check!!!""")
    exit(-1)
  r=re.compile(r"open\(\'(.+).png")
  li=re.findall(r,page)
  return li



#Parse the ss:// string.

def _Parse_QR(subpath):
  config_id={}
  path="https://www.shadowsocks.net/"
  path+=subpath
  path+=".png"
#  print path
  result = _Decodeqr(path)
  if result:# not Null
    ssurl=result['QRCODE']
    ssurl=ssurl[5::]
    try:
      ssurl=base64.b64decode(ssurl)
    except TypeError:
      missing_padding = 4 - len(ssurl) % 4
      ssurl+=missing_padding*"="
#      print ssurl
      ssurl=base64.b64decode(ssurl)
#    else:
    for index,ch in enumerate(special_char):
      pos=ssurl.find(ch)
      config_id[special_corresp[index]]=ssurl[:pos]
      ssurl=ssurl[pos+1::]
    config_id[special_corresp[index+1]]=ssurl
    return config_id

def _Config_proxy():
  socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", local_port)
  socket.socket = socks.socksocket
def _Disable_proxy():
  socket.socket = None

def _Check_Speed_():
  speed=[]
  for i in range(Speed_check_number):
    try:
      start = datetime.datetime.now()
      content = urllib2.urlopen('https://www.google.com',None,3).read()
#      print content
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
  return sum(speed)/Speed_check_number

#print _Check_Speed_()
def _Check_From_File(filename="id.ini"):
  config = open(filename,"r")
  content = config.readlines()
  content = [co[:-1:] for co in content]
  return content
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


def _Check_Content(content):
  for fo in content:
    print(fo)


def _Construct_id(config_li):
    str_li=[]
    str_li.append("sslocal")
#    str_li.append(_config_li["ip"])
    str_li.append("-s")
    str_li.append(config_li["ip"])
    str_li.append("-p")
    str_li.append(config_li["port"])
    str_li.append("-k")
    str_li.append(config_li["password"])
    str_li.append("-m")
    str_li.append(config_li["encry"])
    str_li.append("-l")
    str_li.append(str(local_port))
    return str_li

def foo():
#  _Check_Content()
  png_path=_Get_QR_Png() 
  content=_Check_From_File()
  length = len(content)
  iter_i = 0
  temp = []
  temp = content
  max_speed=0
  temp_speed=0.0
  max_config=[]
  nex=0
  ip2str={}
  print("============QR Check==========")
  for subpath in png_path:
    qr_config_id=_Parse_QR(subpath)
    print qr_config_id
    if qr_config_id:
      _str_li = _Construct_id(qr_config_id)
      ip2str[qr_config_id["ip"]]=_str_li
  for key in ip2str:
      child=subprocess.Popen(ip2str[key])
      os.system("sleep 2")
      _Config_proxy()
      temp_speed = _Check_Speed_()
      print("IP:%s 's speed %d \n"%(key,temp_speed))
      child.kill()
      if temp_speed > max_speed:
        max_config=ip2str[key][:]
        max_speed=temp_speed

  print("============id.ini Check==========")
  while iter_i < length:
    _str_li=[]
    _config_li= _Read_One_Item(temp,5)
    _str_li = _Construct_id(_config_li)
    child=subprocess.Popen(_str_li)
    os.system("sleep 2")
    _Config_proxy()
    temp_speed = _Check_Speed_()
    print("IP:%s 's speed %d \n"%(_config_li["ip"],temp_speed))
    child.kill()
    if temp_speed > max_speed:
       max_config=_str_li[:]
       max_speed=temp_speed
#       max_str_config=str_li
#    print iter_i
    iter_i+=5
    temp=temp[5: ]
    nex += 1
  Fnull = open("/dev/null","w")
  print("WIN: %s -- %d\n"%("".join(max_config),max_speed))
  child=subprocess.Popen(max_config,stdout=Fnull)

def Check_sslocal():
  global sslocal_flag
  for path in os.environ['PATH'].split(':'):
    if os.path.isdir(path) and 'sslocal' in os.listdir(path):
      sslocal_flag=True
      break
  if not sslocal_flag:
    print("Install shadowsocks first!")
    exit(1)



if __name__ == '__main__':
  Check_sslocal()
  foo()
