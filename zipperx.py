#!/usr/bin/env python3


import random
import sys,os
import py7zr 
import filetype
from itertools import product
import string
import zipfile
from tqdm import tqdm

rarcker_text = """                                  
      _                            
     (_)                           
  _____ _ __  _ __   ___ _ ____  __
 |_  / | '_ \| '_ \ / _ \ '__\ \/ /
  / /| | |_) | |_) |  __/ |   >  < 
 /___|_| .__/| .__/ \___|_|  /_/\_\
       | |   | |                   
       |_|   |_|      v 0.1.0      

===================================

"""

def version():
    ver_text = """
    Zipperx version 0.1.0
    Tested in :  Python 3.9.0 
                 Linux kali 5.10.0-kali3-amd64 #1 SMP Debian 5.10.13-1kali1 (2021-02-08) x86_64 GNU/Linux
    with external library : py7zr, tqdm, zipfile, filetype"""
    print(ver_text)

def help():
   help_text = """
   Zipperx version 0.1.0
   Tested in : Python 3.9.0 
               Linux kali 5.10.0-kali3-amd64 #1 SMP Debian 5.10.13-1kali1 (2021-02-08) x86_64 GNU/Linux
   with external library : py7zr, tqdm, zipfile, filetype, itertools
   Current Supported file type : 7z , zip
   Usage : zipperx.py [program mode] -f [zip files_dir] -w [wordlist_dir]
   
   PROGRAM MODE
    -g [char len] [spec]   : Generate a wordlist
    -b          : Brute forcing zip files with wordlist
    -a [str]    : append a word into your wordlist
    -d          : bruteforcing with default wordlist (./wordlist/rockyou.txt)

   FLAG
    -f [filename]   : Filename target
    -w [wordlist]	: Wordlist to use in bruteforce mode or append mode
    -h , --help 	: Help page
    -v , --version  : check program Version
    
   WORDLIST SPECIFICATION
    l   : Include Letter Lowercase
    u   : include Letter Uppercase
    s   : Include Symbols
    n   : include number
    
    EXAMPLES : zipperx.py -g 12 lusn -f 
             : zipperx.py -b -f /a.zip -w ~/wordlist.txt 
             : zipperx.py -a new_word -w ~/wordlist.txt
             : zipperx.py -d -f /a.7z 
    
    Check the repository at (https://github.com/cap10jack/rarcker)
    """
   print(rarcker_text)
   print(help_text)

#work correctly
def brute_zip(wordlist,filename):
  print(rarcker_text)
  print("\033[0;32;40m [+]"," Cracking password , Grab your coffee ...")
  n_words = len(list(open(wordlist, "rb")))
  file = zipfile.ZipFile(filename)
  with open(wordlist, "rb") as wordlist:
    for word in tqdm(wordlist, total=n_words, unit=" word"):
        try:
            file.extractall(pwd=word.strip())
        except:
            continue
        else:
            print("\033[0;32;40m [+]","\n\033[0;32;40m [+]"," Password found:", word.decode().strip(),'\n\033[0;32;40m [+]",')
            exit()
  print("\033[0;31;40m [!] Password not Found in this Wordlist") 

#work correctly
def brute_7zip(wordlist,filename): 
  print(rarcker_text)
  n_words = len(list(open(wordlist, "rb")))
  print("\033[0;32;40m [+]"," Cracking password , Grab your coffee ...")
  with open(wordlist, "r") as wordlist:
    for word in tqdm(wordlist, total=n_words, unit="word"):
        try:
          file = py7zr.SevenZipFile(filename,password=word.strip())
          file.extractall()
        except:
          continue
        else:
          print("\033[0;32;40m [+]","\n\033[0;32;40m [+]"," Password found:", word.strip(),'\n\033[0;32;40m [+]")
          exit(0)
          break
  print("\033[0;31;40m [!] Password not Found in current Wordlist")  

#work Correctly
def append_mode(word,filename):
  print(rarcker_text)
  with open(filename,'a') as f:
    f.write('\n'+word)
  print("\033[0;32;40m [+]"," word Appended at ",filename )
  print("\033[0;32;40m [+]"," Exiting...")
  exit()

def generate_word(filename,n,spec):
  print(rarcker_text)
  character = ""
  if 'l' in spec:
  	character += string.ascii_lowercase
  if 'u' in spec:
	  character += string.ascii_uppercase
  if 's' in spec:
  	character += string.punctuation
  if ('n' in spec):
  	character += string.digits

  counter = 0
  f = open(filename, 'w')

  for j in tqdm(product(character,repeat=n), total=counter, unit="word"):
    word = "".join(j)
    f.write(word)
    f.write('\n')
    counter+=1
  print("\033[0;32;40m [+]"," Wordlist of {} passwords created".format(counter))
  print("\033[0;32;40m [+]"," Output file : {}".format(filename))
  f.close()
  exit(0)

def main():
  if ("-h" in sys.argv) or ("--help" in sys.argv):
      help()
      sys.exit()
  if ("-v" in sys.argv) or ("--version" in sys.argv):
      version()
      sys.exit()

  #Brute force Mode
  if ("-d" in sys.argv) or ("-b" in sys.argv):
    # Filename Error handling
    try:
      os.path.exists(sys.argv[sys.argv.index('-f')+1])
    except:
      print("\033[0;31;40m [!] ERROR Filename not defined")
      print("\033[0;31;40m [!] Exiting...")
      sys.exit(-1)


    filename = sys.argv[sys.argv.index('-f')+1]
    if ("-d" in sys.argv):
      wordlist = 'wordlist/rockyou.txt'
    elif "-b" in sys.argv:
      # wordlist Error handling
      try:
        os.path.exists(sys.argv[sys.argv.index('-w')+1])
      except:
        print("\033[0;31;40m [!] ERROR Wordlist is not defined")
        print("\033[0;31;40m [!] Exiting...")
        sys.exit(-1)
      wordlist = sys.argv[sys.argv.index('-w')+1]



    datatype = filetype.guess(filename)

    # Data type error handling
    if datatype is None:
      print("\033[0;31;40m [!] ERROR Cannot detect data type of input file ")
      print("\033[0;31;40m [!] Exiting...")
      sys.exit(-1)

    #Data Extension dectection
    if datatype.extension == '7z':
      brute_7zip(wordlist,filename)
      sys.exit()
    elif datatype.extension == 'zip':
      brute_zip(wordlist,filename)
      sys.exit()
    else:
      print("\033[0;31;40m [!] ERROR Filetype is not supported")
      print("\033[0;31;40m [!] Exiting...")
      sys.exit(-1)

  #Generate Mode
  if ("-g" in sys.argv):
    # Error handling
    try:
        os.path.exists(sys.argv[sys.argv.index('-g')+1])
    except:
        print("\033[0;31;40m [!] ERROR wordlist specification is not defined")
        print("\033[0;31;40m [!] Exiting...")
        sys.exit(-1)
    try:
    	filename = sys.argv[sys.argv.index('-f')+1]
    except:
    	filename = 'wordlist/generated_wordlist.txt'	 
    spec = sys.argv[sys.argv.index('-g')+2]
    n = int(sys.argv[sys.argv.index('-g')+1])
    generate_word(filename,n,spec)

  #Append mode
  if ('-a' in sys.argv):
    try:
        os.path.exists(sys.argv[sys.argv.index('-a')+1])
    except:
        print("\033[0;31;40m [!] ERROR string is not defined")
        print("\033[0;31;40m [!] Exiting...")
        sys.exit(-1)
    try:
        os.path.exists(sys.argv[sys.argv.index('-w')+1])
    except:
        print("\033[0;31;40m [!] ERROR file target is not defined")
        print("\033[0;31;40m [!] Exiting...")
        sys.exit(-1) 
    word = sys.argv[sys.argv.index('-a')+1]
    file = sys.argv[sys.argv.index('-w')+1]
    append_mode(word,file)
    sys.exit(0)

  print("Usage : rarcker.py [program mode] -f [rar files_dir] -w [wordlist_dir]\n--help , -h for more Information")


if __name__ == "__main__":
    main()
