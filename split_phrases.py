#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import string
import re
import codecs

def merge_phrases(phrase_list, max_len=80):
  long_phrase = ''
  for phrase in phrase_list:
    if phrase == '.' or phrase == ',' or phrase == '!' or phrase == '?':
      long_phrase += phrase
      continue
    
    if (len(phrase) + len(long_phrase)) > max_len:
      yield long_phrase
      long_phrase = phrase
    else:
      if long_phrase:
	long_phrase += " "
      long_phrase += phrase
  
  if long_phrase:
    yield long_phrase
     

def main():
  max_len = int(sys.argv[2])
  with codecs.open(sys.argv[1],'r', 'utf-8') as content_file:
    content = content_file.read()
    
    for line in content.splitlines():
      if line:
	(person, c, text) = line.partition(":")
	
	if not person:
	  continue
	
	phrase_list = [l.strip() for l in re.split("(\.|,|!|\?)", text) if l]
	
	for phrase in merge_phrases(phrase_list, max_len):
	  if phrase.endswith(('.',',')):
	    phrase=phrase[:-1]
	  if phrase:
	    print person.encode("utf-8"), ":", phrase.encode("utf-8")
	  

if __name__ == "__main__":
  main()
  
  

	

