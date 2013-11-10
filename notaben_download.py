#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import string
import re
import urllib2
import multiprocessing
import os.path

def get_chapter(book, match_objects):
  for m in match_objects:
    yield (book, m.group(1), m.group(2))

def download(chapter):
  book,group, name = chapter
  
  filename = ''.join(name.split()) + '.txt'
  if os.path.isfile(filename):
    return
 
  print filename
    
  txt_file = urllib2.urlopen('http://notabenoid.com/book/'+book+'/'+group+'/download?format=t&enc=UTF-8')
  output = open(filename,'wb')
  output.write(txt_file.read())
  output.close()

def main():
  book = sys.argv[1]
  response = urllib2.urlopen('http://notabenoid.com/book/'+book)
    
  content = response.read()
  p = multiprocessing.Pool(5)
  p.map(download, get_chapter(book, re.finditer("/book/%s/([0-9]+)'>.*?(Episode [0-9]+).*?</a>"%book,content)))
     
if __name__ == "__main__":
  main()
    