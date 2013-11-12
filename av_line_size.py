#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import string
import re
import codecs

def main():
  with codecs.open(sys.argv[1],'r', 'utf-8-sig') as content_file:
    content = content_file.read()
    lineCounter = 0;
    lineLength = 0
    minLenght = 10000
    minLine = ''
    for line in content.splitlines():
      if line:
	lineCounter += 1
	(p,c,t) = line.partition(':')
	lineLength += len(t)
	if len(t) < minLenght:
	  minLenght = len(t)
	  minLine = line
	
    if sys.argv[2] == 'm':
      if minLenght < int(sys.argv[3]):
	print sys.argv[1], minLenght, ':', minLine.encode('utf-8')
    else:
      print lineLength/lineCounter
      
if __name__ == "__main__":
  main()
    
    
	
	
