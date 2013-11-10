#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import string
import re
import codecs

def hasSeeTommorow(line):
  seeTommorow = [u'В завтрашн',
		  u'В завтрашн',
		  u'Завтра',
		  u'Сморите завтра',
		  u'Смортите завтра',
		  u'Смотрите завтра',
		  u'Смотрите в завтрашнем',
		  u'в следующей серии',
		  u'в следующем эпизоде',
		  u'в следующий',
		  u'смотрите в',
		  u'в понедельник',
		  u'продолжайте смотреть',
		  u'Смотрите далее',
		  u'Скоро']
  
  l = line.lower().strip()
  for p in seeTommorow:
    if l.startswith(p.lower()):
      return True
    
  return False

def hasFollowing(line):
  follow = [u'Теперь далее',
	    u'Смотрите далее',
	    u'Далее..',
	    u'Далее следует',
	    u'Далее в серии',
	    u'Далее в фильме',
	    u'история продолжается',
	    u'впереди..',
	    u'итак...',
	    u'продолжение...',
	    u'а дальше...',
	    u'теперь дальше',
	    u'смотрите дальше']
  
  l = line.lower()
  for p in follow:
    if re.search(p.lower(), l):
      return True
    
  return False

def hasPrev(line):
  prev = [u'Ранее',
	  u'В предыдущих сериях',
	  u'До этого',
	  u'В предыдущих эпизодах']
  
  l = line.lower().strip()
  for p in prev:
    if l.startswith(p.lower()):
      return True
    
  return False

def merge_phrases(phrase_list, max_len=80):
  long_phrase = ''
  for phrase in phrase_list:
    if re.search('^[.,!?]$',phrase):
      long_phrase += phrase
      continue

    if (len(phrase) + len(long_phrase)) > max_len:
      yield long_phrase
      long_phrase = phrase
    else:
      long_phrase += " "
      long_phrase += phrase
  
  if long_phrase:
    yield long_phrase
       
def merge_punctuation(phrase_list):
  real_phrase = ''
  for phrase in phrase_list:
    real_phrase += phrase
    
    if re.search('^[.!;?]+$',phrase):
      yield real_phrase
      real_phrase = ''
  
  if real_phrase:
    yield real_phrase
  
def split_phrase(phrase, max_len=80):
  if len(phrase) < max_len or not re.search(',',phrase):
    yield phrase
  else:
    (left, c, right) = phrase.rpartition(',')
    
    while len(left) > max_len and re.search(',',left):
      (left, c, r) = left.rpartition(',')
      right = r + ',' + right
      
    yield left
      
    for val in split_phrase(right, max_len):
      yield val
    
def main():
  max_len = int(sys.argv[2])
  
  with codecs.open(sys.argv[1],'r', 'utf-8-sig') as content_file:
    content = content_file.read()
    
    notHeroes = [u'переводчики', u'рассказчик', u'переводчик']
        
    states = {'prev': 0, 'next':1,'split':2, 'sureSplit':3}
    curState = states['prev']
    
    outLines = []
    lineCounter = 0
    
    log_file = codecs.open('log.txt', 'a', 'utf-8')
    log_file.write(sys.argv[1] + '\n')
    for line in content.splitlines():
      if line:
	lineCounter += 1
	
	if curState == states['prev'] and hasPrev(line):
	  curState = states['next']
	  log_file.write(sys.argv[1] + u': found ранее at string ' + str(lineCounter) + '\n') 
	elif curState != states['sureSplit']:
	  curState = states['split']
	
	if curState == states['next']:
	  if hasFollowing(line):
	    curState = states['split']
	    log_file.write(sys.argv[1] + u': found далее at string ' + str(lineCounter) + '\n')
	  continue
	
	if curState == states['split'] and hasFollowing(line) and lineCounter < 15:
	  log_file.write(sys.argv[1] + u': dropping prev strings as found далее at string, ' + str(lineCounter) + '\n')
	  outLines = []
	  curState = states['sureSplit']
	  continue
	
	line = ' '.join(line.split())
	
	(person, c, text) = line.partition(":")
	
	person = person.strip()
	
	if hasSeeTommorow(person):
	  log_file.write(sys.argv[1] + u': found завтра at string ' + str(lineCounter) + '\n')
	  break
	
	if not person or person.startswith('http'):
	  continue
	
	if person.lower() in notHeroes:
	  continue
	
	personName = person.encode("utf-8")
	
	phrase_list = [l.strip() for l in re.split("([.;!?]+)", text) if l]
	
	should_add_line = False
	
	for phrase in merge_punctuation(phrase_list):
	  phrase = phrase.strip()
	  if phrase.endswith('.') and not phrase.endswith('..'):
	    phrase = phrase.rstrip('.')
	    
	  if phrase:
	    for sub_phrase in split_phrase(phrase, max_len):
	      outLines.append(personName + ' : ' + sub_phrase.strip().rstrip(",").encode("utf-8"))
	      
	    should_add_line = True
	
	if should_add_line:
	  outLines.append('')
	  
    for line in outLines:
      print line
      
    log_file.write('\n')
    log_file.close()

if __name__ == "__main__":
  main()
  
  

	

