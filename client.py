#!/usr/bin/env python 

""" 
Hangman client 
Author: Karthik
""" 

import socket 
import sys
import re

host = 'localhost' 
port = 50000 
size = 1024 
print "Welcome to Hangman-Movies!\nEnter the missing letters to complete the movie name\nCntrl+C to exit the game\n"
tmp_output = ""
tmp_input = ""
while 1:
    try:
        print "Welcome to Hangman-Movies!\nEnter one letter at a time to complete the movie name\n"
        entered_letters = []
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.connect((host,port))
        output = s.recv(size)
        s.close() 
        wrong_guesses = 0
        while output.find("*") != -1:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            s.connect((host,port))
            output = s.recv(size)
            if output: 
                if output.find("*") != -1:
                    if output == tmp_output:
                        wrong_guesses += 1
                        if entered_letters:
                            if entered_letters.count(tmp_input) != 0:
                                print "\nLetter \'",tmp_input,"\' was entered previously. Try a different letter\n"
                            elif entered_letters.count(tmp_input) == 0:
                                print "\nLetter \'",tmp_input,"\' not found. Keep guessing\n"
                        else:                    
                            print "\nLetter \'",tmp_input,"\' not found. Keep guessing\n"
                    print output
                    if tmp_input:
                        duplicate_index = entered_letters.count(tmp_input.rstrip())
                        if duplicate_index == 0:
                            entered_letters.append(tmp_input.rstrip())
                    if entered_letters:
                        entered_letters_string = ""
                        for letter in entered_letters:
                            entered_letters_string += letter.rstrip()
                            entered_letters_string += " "
                        print "\nEntered letters: ",entered_letters_string
                    data = raw_input("\nEnter a letter: ")
                    match = re.search(r'[^\W\d_]',data)
                    while not(match) or len(data) != 1:
                        print 'Only letters are allowed. Please re-enter the letter\n'
                        data = raw_input("\nEnter a letter: ")
                        match = re.search(r'[^\W\d_]',data)
                    tmp_input = data
                    s.send(data)
                else:
                    print "****  Bingo! The movie name is",output," ****"
                    print "Number of Incorrect guesses is ",wrong_guesses,"\n\n***************************************\n\n"
                    break
            tmp_output = output        
            s.close()
    except KeyboardInterrupt:
        print "\nExiting...\n"
        sys.exit(0) 
