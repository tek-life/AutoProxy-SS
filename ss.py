
config = open("id.ini","r")
content = config.readlines()
content = [co[:-1:] for co in content]

def _Read_One_Item(list_part, num):
  if num < 4:
    print("Error! The item is wrong\n")
    exit(-1);
  ip=list_part[0]
  port=list_part[1]
  password=list_part[2]
  encry = list_part[3]
  supporter = list_part[4]
#  print [ip,port,password,encry,supporter]
  return [ip,port,password,encry,supporter]



def _Check_Content():
  for fo in content:
    print fo

def foo():
#  _Check_Content()
  length = len(content)
  iter_i = 0
  temp = []
  temp = content
  while iter_i < length:
    print _Read_One_Item(temp,5)
#    print iter_i
    iter_i+=5
    temp=temp[5: ]

if __name__ == '__main__':
  foo()
